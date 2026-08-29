<?php
// ============================================================
// Yanagiya Reservation System — PHP Proxy
// ============================================================

// GASのURL（ここだけに書く。HTMLには書かない）
define('GAS_URL', 'https://script.google.com/macros/s/AKfycbyLNQAVHbXv2taAX9WY0IYpGGuX-Bx2LJRvhJo1l4SNCu7AlrJuCODUnuGN9H7QKvnF/exec');

// レート制限
// GET（空席確認）: 1分60回まで（日付をスクロールしても引っかからない）
// POST（予約送信）: 1分10回まで
define('RATE_LIMIT_GET', 60);
define('RATE_LIMIT_POST', 10);
define('RATE_WINDOW', 60); // 秒

// CORS設定
$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
$host = isset($_SERVER['HTTP_HOST']) ? $_SERVER['HTTP_HOST'] : '';
$scheme = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
$allowed_origins = array(
    'https://table.magome-yanagiya.com',
    'https://www.table.magome-yanagiya.com',
    $scheme . '://' . $host,
);

if ($origin !== '' && !in_array($origin, $allowed_origins, true)) {
    http_response_code(403);
    header('Content-Type: application/json');
    echo json_encode(array('error' => 'Forbidden', 'origin' => $origin));
    exit;
}

if ($origin !== '') {
    header('Access-Control-Allow-Origin: ' . $origin);
}
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'unknown';
$method = isset($_SERVER['REQUEST_METHOD']) ? $_SERVER['REQUEST_METHOD'] : 'GET';
$rate_key = sys_get_temp_dir() . '/yanagiya_rate_' . md5($ip . $method);
$rate_limit = ($method === 'POST') ? RATE_LIMIT_POST : RATE_LIMIT_GET;
$now = time();
$requests = array();
if (file_exists($rate_key)) {
    $stored = file_get_contents($rate_key);
    $requests = json_decode($stored, true);
    if (!is_array($requests)) {
        $requests = array();
    }
}

$filtered = array();
foreach ($requests as $timestamp) {
    if (($now - $timestamp) < RATE_WINDOW) {
        $filtered[] = $timestamp;
    }
}
$filtered[] = $now;
file_put_contents($rate_key, json_encode(array_values($filtered)));

if (count($filtered) > $rate_limit) {
    http_response_code(429);
    echo json_encode(array('error' => 'Too many requests. Please try again later.'));
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $date = isset($_GET['date']) ? $_GET['date'] : '';
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) {
        http_response_code(400);
        echo json_encode(array('error' => 'Invalid date format'));
        exit;
    }

    $url = GAS_URL . '?action=availability&date=' . urlencode($date);
    $curlError = null;
    $response = curl_get($url, $curlError);
    if ($response === false) {
        http_response_code(502);
        error_log('Yanagiya proxy GET failed: ' . $curlError);
        echo json_encode(array('error' => 'Failed to reach reservation server', 'details' => $curlError));
        exit;
    }
    if (preg_match('/^\s*</', $response)) {
        http_response_code(502);
        error_log('Yanagiya proxy GET returned HTML response: ' . substr($response, 0, 200));
        echo json_encode(array('error' => 'Invalid reservation server response', 'details' => substr(strip_tags($response), 0, 200)));
        exit;
    }
    echo $response;
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = file_get_contents('php://input');
    $data = json_decode($body, true);
    if (!is_array($data)) {
        http_response_code(400);
        echo json_encode(array('error' => 'Invalid request body'));
        exit;
    }

    $action = isset($data['action']) ? $data['action'] : '';
    if (in_array($action, array('admin_reservations', 'admin_cancel', 'admin_block_slot', 'admin_stats'), true)) {
        $curlError = null;
        $response = curl_post(GAS_URL, json_encode($data), $curlError);
        if ($response === false) {
            http_response_code(502);
            error_log('Yanagiya proxy POST failed: ' . $curlError);
            echo json_encode(array('success' => false, 'message' => 'Failed to reach reservation server.', 'details' => $curlError));
            exit;
        }
        if (preg_match('/^\s*</', $response)) {
            http_response_code(502);
            error_log('Yanagiya proxy POST returned HTML response: ' . substr($response, 0, 200));
            echo json_encode(array('success' => false, 'message' => 'Invalid reservation server response', 'details' => substr(strip_tags($response), 0, 200)));
            exit;
        }
        echo $response;
        exit;
    }

    $date = isset($data['date']) ? $data['date'] : '';
    $meal = isset($data['meal']) ? $data['meal'] : '';
    $time = isset($data['time']) ? $data['time'] : '';
    $partySize = isset($data['partySize']) ? $data['partySize'] : 0;
    $name = isset($data['name']) ? trim($data['name']) : '';

    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) {
        http_response_code(400);
        echo json_encode(array('success' => false, 'message' => 'Invalid date.'));
        exit;
    }

    if ($meal !== 'dinner') {
        http_response_code(400);
        echo json_encode(array('success' => false, 'message' => 'Invalid meal type.'));
        exit;
    }

    $valid_times = array('17:30', '19:00');
    if (!in_array($time, $valid_times, true)) {
        http_response_code(400);
        echo json_encode(array('success' => false, 'message' => 'Invalid time slot.'));
        exit;
    }

    $partySize = intval($partySize);
    if ($partySize < 1 || $partySize > 8) {
        http_response_code(400);
        echo json_encode(array('success' => false, 'message' => 'Invalid party size.'));
        exit;
    }

    if ($name === '' || mb_strlen($name) > 50) {
        http_response_code(400);
        echo json_encode(array('success' => false, 'message' => 'Invalid name.'));
        exit;
    }

    $payload = json_encode(array(
        'action' => 'reserve',
        'date' => $date,
        'meal' => $meal,
        'time' => $time,
        'partySize' => $partySize,
        'name' => htmlspecialchars($name, ENT_QUOTES, 'UTF-8'),
    ));

    $curlError = null;
    $response = curl_post(GAS_URL, $payload, $curlError);
    if ($response === false) {
        http_response_code(502);
        error_log('Yanagiya proxy POST failed: ' . $curlError);
        echo json_encode(array('success' => false, 'message' => 'Failed to reach reservation server.', 'details' => $curlError));
        exit;
    }
    if (preg_match('/^\s*</', $response)) {
        http_response_code(502);
        error_log('Yanagiya proxy POST returned HTML response: ' . substr($response, 0, 200));
        echo json_encode(array('success' => false, 'message' => 'Invalid reservation server response', 'details' => substr(strip_tags($response), 0, 200)));
        exit;
    }

    echo $response;
    exit;
}

http_response_code(405);
echo json_encode(array('error' => 'Method not allowed'));

function curl_get($url, &$error = null) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Yanagiya-Proxy/1.0');
    $res = curl_exec($ch);
    if ($res === false) {
        $error = curl_error($ch);
    }
    curl_close($ch);
    return $res;
}

function curl_post($url, $body, &$error = null) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: text/plain'));
    curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Yanagiya-Proxy/1.0');
    $res = curl_exec($ch);
    if ($res === false) {
        $error = curl_error($ch);
    }
    curl_close($ch);
    return $res;
}
