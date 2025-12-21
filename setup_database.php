<?php
// setup_database.php - One-time script to create database table
// ⚠️ DELETE THIS FILE after successful setup for security!
//
// IMPORTANT:
// - Do NOT keep credentials in this file.
// - Create `db_config.php` next to this file (NOT committed) OR set env vars.

$configFile = __DIR__ . '/db_config.php';
$dbConfig = null;
if (is_readable($configFile)) {
    $dbConfig = require $configFile;
}

$db_host = $dbConfig['host'] ?? getenv('DB_HOST') ?: 'localhost';
$db_name = $dbConfig['name'] ?? getenv('DB_NAME') ?: '';
$db_user = $dbConfig['user'] ?? getenv('DB_USER') ?: '';
$db_pass = $dbConfig['pass'] ?? getenv('DB_PASS') ?: '';

if ($db_name === '' || $db_user === '' || $db_pass === '') {
    echo "<p style='color: red;'>✗ Missing DB config. Create db_config.php or set DB_NAME/DB_USER/DB_PASS env vars.</p>";
    exit();
}

echo "<h1>Database Setup Script</h1>";
echo "<p>Attempting to connect and create table...</p>";

try {
    // Connect to database
    $pdo = new PDO(
        "mysql:host=$db_host;dbname=$db_name;charset=utf8mb4",
        $db_user,
        $db_pass,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]
    );
    
    echo "<p style='color: green;'>✓ Connected to database successfully!</p>";
    
    // Create table SQL
    $sql = "CREATE TABLE IF NOT EXISTS experiment_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        participant_id VARCHAR(100),
        `condition` VARCHAR(50),
        submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        task_data JSON,
        freeplay_data JSON,
        user_agent TEXT,
        screen_resolution VARCHAR(50),
        INDEX idx_participant (participant_id),
        INDEX idx_condition (`condition`),
        INDEX idx_time (submission_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";
    
    $pdo->exec($sql);
    
    echo "<p style='color: green;'>✓ Table 'experiment_data' created successfully!</p>";
    
    // Verify table exists
    $result = $pdo->query("SHOW TABLES LIKE 'experiment_data'");
    if ($result->rowCount() > 0) {
        echo "<p style='color: green;'>✓ Table verified - setup complete!</p>";
        echo "<h2 style='color: red;'>⚠️ IMPORTANT: DELETE THIS FILE NOW FOR SECURITY!</h2>";
        echo "<p>You can now use your experiment. Remember to delete setup_database.php from your server.</p>";
    } else {
        echo "<p style='color: red;'>✗ Table verification failed</p>";
    }
    
    // Show table structure
    echo "<h3>Table Structure:</h3>";
    $columns = $pdo->query("DESCRIBE experiment_data")->fetchAll();
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th></tr>";
    foreach ($columns as $col) {
        echo "<tr>";
        echo "<td>{$col['Field']}</td>";
        echo "<td>{$col['Type']}</td>";
        echo "<td>{$col['Null']}</td>";
        echo "<td>{$col['Key']}</td>";
        echo "<td>{$col['Default']}</td>";
        echo "</tr>";
    }
    echo "</table>";
    
} catch (PDOException $e) {
    echo "<p style='color: red;'>✗ Error: " . $e->getMessage() . "</p>";
    echo "<p>Please check your database credentials in this file.</p>";
}
?>
