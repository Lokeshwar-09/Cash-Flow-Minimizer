
php<?php
$conn = new mysqli("localhost", "root", "", "dos_project");

$total   = $conn->query("SELECT COUNT(*) as cnt FROM socket_logs")->fetch_assoc()['cnt'];
$attacks = $conn->query("SELECT COUNT(*) as cnt FROM socket_logs WHERE status='ATTACK_DETECTED'")->fetch_assoc()['cnt'];
$blocked = $conn->query("SELECT COUNT(*) as cnt FROM socket_logs WHERE status='BLOCKED'")->fetch_assoc()['cnt'];
$allowed = $conn->query("SELECT COUNT(*) as cnt FROM socket_logs WHERE status='ALLOWED'")->fetch_assoc()['cnt'];
$logs    = $conn->query("SELECT * FROM socket_logs ORDER BY log_time DESC LIMIT 30");

$atk_ips = $conn->query("SELECT ip_address, COUNT(*) as cnt FROM socket_logs
                          WHERE status='ATTACK_DETECTED'
                          GROUP BY ip_address ORDER BY cnt DESC LIMIT 5");
?>
<!DOCTYPE html>
<html>
<head>
    <title>DoS Protection Dashboard</title>
    <meta http-equiv="refresh" content="3">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #0d0d0d;
            color: #ffffff;
            padding: 24px;
        }
        h1 { color: #00ff88; font-size: 22px; margin-bottom: 4px; }
        .sub { color: #555; font-size: 13px; margin-bottom: 24px; }
        .cards {
            display: flex;
            gap: 16px;
            margin-bottom: 30px;
        }
        .card {
            background: #1a1a1a;
            border-radius: 10px;
            padding: 20px 24px;
            flex: 1;
            text-align: center;
        }
        .card h2 { font-size: 38px; font-weight: 700; margin-bottom: 6px; }
        .card p  { font-size: 13px; color: #777; }
        .green  { color: #00ff88; }
        .red    { color: #ff4444; }
        .orange { color: #ffaa00; }
        .blue   { color: #44aaff; }
        .blink  { animation: blink 1s infinite; }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
        .section-title {
            font-size: 15px;
            color: #aaa;
            margin-bottom: 12px;
            margin-top: 28px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #1a1a1a;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 30px;
        }
        th {
            background: #222;
            padding: 12px 14px;
            text-align: left;
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        td {
            padding: 10px 14px;
            font-size: 13px;
            border-bottom: 1px solid #222;
        }
        .ATTACK_DETECTED { color: #ff4444; font-weight: bold; }
        .BLOCKED         { color: #ffaa00; font-weight: bold; }
        .ALLOWED         { color: #00ff88; }
        .dot {
            display: inline-block;
            width: 8px; height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        .dot-red    { background: #ff4444; }
        .dot-green  { background: #00ff88; }
        .dot-orange { background: #ffaa00; }
    </style>
</head>
<body>

<h1>DoS Protection — Live Dashboard</h1>
<p class="sub">Auto-refreshing every 3 seconds &nbsp;|&nbsp; <?= date('d M Y, H:i:s') ?></p>

<div class="cards">
    <div class="card">
        <h2 class="blue"><?= $total ?></h2>
        <p>Total Requests</p>
    </div>
    <div class="card">
        <h2 class="green"><?= $allowed ?></h2>
        <p>Allowed</p>
    </div>
    <div class="card">
        <h2 class="red <?= $attacks > 0 ? 'blink' : '' ?>"><?= $attacks ?></h2>
        <p>Attacks Detected</p>
    </div>
    <div class="card">
        <h2 class="orange"><?= $blocked ?></h2>
        <p>Blocked</p>
    </div>
</div>

<p class="section-title">Top attacker IPs</p>
<table>
    <tr>
        <th>IP Address</th>
        <th>Attack Count</th>
    </tr>
    <?php while ($row = $atk_ips->fetch_assoc()): ?>
    <tr>
        <td><span class="dot dot-red"></span><?= $row['ip_address'] ?></td>
        <td class="red"><?= $row['cnt'] ?></td>
    </tr>
    <?php endwhile; ?>
</table>

<p class="section-title">Live request log — last 30 events</p>
<table>
    <tr>
        <th>#</th>
        <th>IP Address</th>
        <th>Status</th>
        <th>Requests</th>
        <th>Time</th>
    </tr>
    <?php while ($row = $logs->fetch_assoc()): ?>
    <tr>
        <td style="color:#555"><?= $row['id'] ?></td>
        <td>
            <?php
            if ($row['status'] === 'ALLOWED') echo '<span class="dot dot-green"></span>';
            elseif ($row['status'] === 'ATTACK_DETECTED') echo '<span class="dot dot-red"></span>';
            else echo '<span class="dot dot-orange"></span>';
            ?>
            <?= $row['ip_address'] ?>
        </td>
        <td class="<?= $row['status'] ?>"><?= $row['status'] ?></td>
        <td><?= $row['request_count'] ?></td>
        <td style="color:#555"><?= $row['log_time'] ?></td>
    </tr>
    <?php endwhile; ?>
</table>

</body>
</html>