
php<?php
$conn = new mysqli("localhost", "root", "", "dos_project");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "Inserting Users...<br>";
for ($i = 1; $i <= 5000; $i++) {
    $name = "User" . $i;
    $email = "user" . $i . "@gmail.com";
    $conn->query("INSERT IGNORE INTO users (name, email) VALUES ('$name', '$email')");
}

echo "Inserting Orders...<br>";
for ($i = 1; $i <= 20000; $i++) {
    $user_id = rand(1, 5000);
    $amount = rand(100, 5000);
    $date = date('Y-m-d H:i:s');
    $conn->query("INSERT INTO orders (user_id, amount, order_date) VALUES ($user_id, $amount, '$date')");
}

echo "Done! Data inserted successfully.";
?>