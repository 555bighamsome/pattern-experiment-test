<?php
// migrate_database.php - One-time migration script to rebuild experiment_data table
//
// What it does (safe rebuild):
// 1) Creates experiment_data_new with the desired schema (incl prolific_id + debrief_data)
// 2) Copies rows from experiment_data -> experiment_data_new
//    - Extracts prolific_id from column or from JSON (task/freeplay/debrief)
//    - Extracts debrief_data from task_data.debrief or freeplay_data.debrief
// 3) Verifies row counts
// 4) Renames old table to experiment_data_backup_YYYYMMDD_HHMMSS
// 5) Renames new table to experiment_data
//
// ⚠️ SECURITY:
// - Delete this file after successful migration.
// - Do NOT commit db_config.php.
//
// Requirements:
// - MySQL 5.7+ / MariaDB with JSON support recommended.
// - db_config.php next to this file OR env vars DB_HOST/DB_NAME/DB_USER/DB_PASS.

header('Content-Type: text/plain; charset=utf-8');

function out($msg) {
    echo $msg . "\n";
}

function fail($msg, $code = 1) {
    out("✗ ERROR: " . $msg);
    exit($code);
}

function parseJsonIfString($value) {
    if ($value === null) return null;
    if (is_array($value)) return $value;
    if (is_string($value)) {
        $trimmed = trim($value);
        if ($trimmed === '') return null;
        $decoded = json_decode($trimmed, true);
        if (json_last_error() === JSON_ERROR_NONE) return $decoded;
    }
    return null;
}

function firstNonEmptyString($candidates) {
    foreach ($candidates as $c) {
        if (is_string($c)) {
            $v = trim($c);
            if ($v !== '') return $v;
        }
    }
    return null;
}

function getNested($arr, $path) {
    // $path like ['debrief','prolificId']
    $cur = $arr;
    foreach ($path as $k) {
        if (!is_array($cur) || !array_key_exists($k, $cur)) return null;
        $cur = $cur[$k];
    }
    return $cur;
}

out("=== experiment_data migration (safe rebuild) ===");
out("Time: " . date('c'));

// Load DB config
$configFile = __DIR__ . '/db_config.php';
$dbConfig = null;
if (is_readable($configFile)) {
    $dbConfig = require $configFile;
    if (!is_array($dbConfig)) {
        fail('db_config.php must return an array.');
    }
}

$db_host = $dbConfig['host'] ?? getenv('DB_HOST') ?: 'localhost';
$db_name = $dbConfig['name'] ?? getenv('DB_NAME') ?: '';
$db_user = $dbConfig['user'] ?? getenv('DB_USER') ?: '';
$db_pass = $dbConfig['pass'] ?? getenv('DB_PASS') ?: '';

if ($db_name === '' || $db_user === '' || $db_pass === '') {
    fail('Missing DB config. Create db_config.php or set DB_NAME/DB_USER/DB_PASS env vars.');
}

try {
    $pdo = new PDO(
        "mysql:host=$db_host;dbname=$db_name;charset=utf8mb4",
        $db_user,
        $db_pass,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]
    );
} catch (PDOException $e) {
    fail('DB connection failed: ' . $e->getMessage());
}

out("✓ Connected to DB '$db_name' at '$db_host'");

// Ensure source table exists
$exists = $pdo->query("SHOW TABLES LIKE 'experiment_data'")->rowCount() > 0;
if (!$exists) {
    fail("Source table 'experiment_data' does not exist.");
}

// Prevent overwriting an existing new table
$existsNew = $pdo->query("SHOW TABLES LIKE 'experiment_data_new'")->rowCount() > 0;
if ($existsNew) {
    fail("Table 'experiment_data_new' already exists. Delete/rename it first.");
}

// Create new table schema
out('Creating experiment_data_new...');
$createSql = "CREATE TABLE experiment_data_new (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id VARCHAR(100) NOT NULL,
    prolific_id VARCHAR(64) NULL,
    `condition` VARCHAR(50) NOT NULL,
    submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_data JSON NULL,
    freeplay_data JSON NULL,
    debrief_data JSON NULL,
    user_agent TEXT NULL,
    screen_resolution VARCHAR(50) NULL,
    INDEX idx_participant (participant_id),
    INDEX idx_prolific (prolific_id),
    INDEX idx_condition (`condition`),
    INDEX idx_time (submission_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";
$pdo->exec($createSql);
out('✓ Created experiment_data_new');

// Read all rows from old table
out('Reading rows from experiment_data...');
$rows = $pdo->query('SELECT * FROM experiment_data ORDER BY id ASC')->fetchAll();
$outCount = count($rows);
out("✓ Found $outCount rows");

// Prepare insert
$ins = $pdo->prepare(
    "INSERT INTO experiment_data_new
    (participant_id, prolific_id, `condition`, submission_time, task_data, freeplay_data, debrief_data, user_agent, screen_resolution)
    VALUES
    (:participant_id, :prolific_id, :condition, :submission_time, CAST(:task_data AS JSON), CAST(:freeplay_data AS JSON), CAST(:debrief_data AS JSON), :user_agent, :screen_resolution)"
);

out('Migrating rows...');
$pdo->beginTransaction();
try {
    $migrated = 0;

    foreach ($rows as $r) {
        $participantId = $r['participant_id'] ?? null;
        $condition = $r['condition'] ?? ($r['condition'] ?? null);
        // In some schemas, column may be named `condition` exactly; PHP array key is 'condition'
        if ($condition === null && array_key_exists('condition', $r)) {
            $condition = $r['condition'];
        }
        $submissionTime = $r['submission_time'] ?? null;
        $userAgent = $r['user_agent'] ?? null;
        $screenRes = $r['screen_resolution'] ?? null;

        // Task/freeplay JSON might be returned as string (depending on PDO/mysql). Normalize.
        $taskRaw = $r['task_data'] ?? null;
        $freeRaw = $r['freeplay_data'] ?? null;
        $taskObj = parseJsonIfString($taskRaw);
        $freeObj = parseJsonIfString($freeRaw);

        // Extract debrief
        $debriefObj = null;
        if (is_array($taskObj)) {
            $debriefObj = $taskObj['debrief'] ?? null;
        }
        if ($debriefObj === null && is_array($freeObj)) {
            $debriefObj = $freeObj['debrief'] ?? null;
        }
        $debriefObj = is_array($debriefObj) ? $debriefObj : null;

        // Extract prolificId from:
        // 1) existing column prolific_id if present
        // 2) taskObj.prolificId / freeObj.prolificId
        // 3) debriefObj.prolificId
        $prolificFromCol = null;
        if (array_key_exists('prolific_id', $r)) {
            $prolificFromCol = $r['prolific_id'];
        }
        $prolific = firstNonEmptyString([
            $prolificFromCol,
            is_array($taskObj) ? ($taskObj['prolificId'] ?? null) : null,
            is_array($freeObj) ? ($freeObj['prolificId'] ?? null) : null,
            is_array($debriefObj) ? ($debriefObj['prolificId'] ?? null) : null,
        ]);

        // If participant_id missing, skip row (shouldn't happen)
        if ($participantId === null || trim((string)$participantId) === '') {
            continue;
        }
        if ($condition === null || trim((string)$condition) === '') {
            $condition = 'unknown';
        }

        // Keep original JSON if possible. If PDO gave us arrays, we need to re-encode.
        $taskJson = $taskObj !== null ? json_encode($taskObj, JSON_UNESCAPED_UNICODE) : null;
        $freeJson = $freeObj !== null ? json_encode($freeObj, JSON_UNESCAPED_UNICODE) : null;
        $debriefJson = $debriefObj !== null ? json_encode($debriefObj, JSON_UNESCAPED_UNICODE) : null;

        // MySQL CAST(:x AS JSON) fails if value is NULL; handle with SQL NULL by binding null.
        $ins->execute([
            ':participant_id' => $participantId,
            ':prolific_id' => $prolific,
            ':condition' => $condition,
            ':submission_time' => $submissionTime,
            ':task_data' => $taskJson,
            ':freeplay_data' => $freeJson,
            ':debrief_data' => $debriefJson,
            ':user_agent' => $userAgent,
            ':screen_resolution' => $screenRes,
        ]);

        $migrated++;
    }

    $pdo->commit();
    out("✓ Migrated $migrated rows into experiment_data_new");
} catch (Exception $e) {
    $pdo->rollBack();
    fail('Migration failed, rolled back. Details: ' . $e->getMessage());
}

// Verify counts
$newCount = (int)($pdo->query('SELECT COUNT(*) AS c FROM experiment_data_new')->fetch()['c'] ?? 0);
$oldCount = (int)($pdo->query('SELECT COUNT(*) AS c FROM experiment_data')->fetch()['c'] ?? 0);

out("Row count check: old=$oldCount new=$newCount");
if ($newCount !== $oldCount) {
    out('⚠ WARNING: Row counts differ. Will NOT swap tables.');
    out("You can inspect experiment_data_new, fix issues, then rerun after cleanup.");
    exit(2);
}

// Swap tables
$backupName = 'experiment_data_backup_' . date('Ymd_His');
out("Swapping tables. Backup will be: $backupName");
try {
    $pdo->exec("RENAME TABLE experiment_data TO $backupName, experiment_data_new TO experiment_data");
    out('✓ Swap complete');
    out('DONE. You can now inspect the new experiment_data table.');
    out('NOTE: The old table is kept as a backup. Delete it only after verifying.');
    out("Backup table name: $backupName");
} catch (PDOException $e) {
    fail('Swap failed: ' . $e->getMessage());
}

?>
