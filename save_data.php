<?php
// save_data.php - Backend API to save experiment data to database
//
// Security notes:
// - Do NOT hard-code DB credentials in this repo.
// - Restrict CORS origins to your deployment domains.
//
// Configure allowed origins (edit to match your GitHub Pages + your server domain)
$allowed_origins = [
    'https://555bighamsome.github.io',
    'https://555bighamsome.github.io/',
    'https://bococo-81.inf.ed.ac.uk',
    'https://bococo-81.inf.ed.ac.uk/',
];

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && in_array($origin, $allowed_origins, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit();
}

// Database configuration
// Preferred: create a file named `db_config.php` next to this file (NOT committed) that returns an array.
// Fallback: environment variables DB_HOST/DB_NAME/DB_USER/DB_PASS.
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
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Server misconfigured: missing DB_NAME/DB_USER/DB_PASS'
    ]);
    exit();
}

try {
    // Connect to database
    $pdo = new PDO(
        "mysql:host=$db_host;dbname=$db_name;charset=utf8mb4",
        $db_user,
        $db_pass,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        ]
    );

    // Get JSON data from request
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if (!$data) {
        throw new Exception('Invalid JSON data');
    }

    // Validate required fields
    if (!isset($data['participantId']) || !isset($data['condition'])) {
        throw new Exception('Missing required fields: participantId or condition');
    }

    // Extract data
    $participant_id = $data['participantId'];
    $condition = $data['condition'];
    $task_data = isset($data['taskData']) ? json_encode($data['taskData']) : null;
    $freeplay_data = isset($data['freeplayData']) ? json_encode($data['freeplayData']) : null;
    $user_agent = isset($data['userAgent']) ? $data['userAgent'] : $_SERVER['HTTP_USER_AGENT'];
    $screen_resolution = isset($data['screenResolution']) ? $data['screenResolution'] : null;

    // Insert into database
    $sql = "INSERT INTO experiment_data 
        (participant_id, `condition`, task_data, freeplay_data, user_agent, screen_resolution) 
        VALUES 
        (:participant_id, :condition, :task_data, :freeplay_data, :user_agent, :screen_resolution)";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        ':participant_id' => $participant_id,
        ':condition' => $condition,
        ':task_data' => $task_data,
        ':freeplay_data' => $freeplay_data,
        ':user_agent' => $user_agent,
        ':screen_resolution' => $screen_resolution
    ]);

    $insert_id = $pdo->lastInsertId();

    // Success response
    echo json_encode([
        'success' => true,
        'message' => 'Data saved successfully',
        'id' => $insert_id
    ]);

} catch (PDOException $e) {
    // Database error
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Database error: ' . $e->getMessage()
    ]);
} catch (Exception $e) {
    // Other errors
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
?>
