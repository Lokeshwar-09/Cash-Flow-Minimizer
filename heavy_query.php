
php<?php
$conn = new mysqli("localhost", "root", "", "dos_project");

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
echo "<br><br>Execution Time: " . round($end - $start, 4) . " seconds";
?>