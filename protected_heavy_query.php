 php<?php
session_start();

$conn = new mysqli("localhost", "root", "", "dos_project");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$max_requests = 5;
$time_window  = 10;

if (!isset($_SESSION['request_count'])) {
    $_SESSION['request_count']    = 1;
    $_SESSION['first_request_time'] = time();
} else {
    if (time() - $_SESSION['first_request_time'] < $time_window) {
        $_SESSION['request_count']++;
    } else {
        $_SESSION['request_count']    = 1;
        $_SESSION['first_request_time'] = time();
    }
}

if ($_SESSION['request_count'] > $max_requests) {
    $ip      = $_SERVER['REMOTE_ADDR'];
    $message = "Rate limit exceeded";
    $stmt    = $conn->prepare("INSERT INTO attack_logs (ip_address, message) VALUES (?, ?)");
    $stmt->bind_param("ss", $ip, $message);
    $stmt->execute();
    $stmt->close();
    die("Too many requests! Attempt logged.");
}

$start = microtime(true);

$sql = "SELECT users.name, SUM(orders.amount) as total
        FROM users
        JOIN orders ON users.id = orders.user_id
        GROUP BY users.id
        HAVING total > 10000
        ORDER BY total DESC";

$result = $conn->query($sql);

while ($row = $result->fetch_assoc()) {
    echo $row["name"] . " - " . $row["total"] . "<br>";
}

$end = microtime(true);

$ip            = $_SERVER['REMOTE_ADDR'];
$query_type    = "HEAVY";
$priority      = "LOW";
$exec_time     = round($end - $start, 4);
$conn->query("INSERT INTO query_scheduler (ip_address, query_type, priority_level, execution_time)
              VALUES ('$ip', '$query_type', '$priority', '$exec_time')");

echo "<br><br>Execution Time: " . $exec_time . " seconds";
?>