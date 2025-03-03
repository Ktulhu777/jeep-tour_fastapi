<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Документация API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #007BFF;
            color: white;
        }
        code {
            background-color: #eee;
            padding: 4px 8px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📌 API документация</h1>
        <p>Этот API предназначен для управления кошельком.</p>
        
        <h2>📍 Эндпоинты</h2>
        <table>
            <tr>
                <th>Метод</th>
                <th>URL</th>
                <th>Описание</th>
            </tr>
            <tr>
                <td><code>GET</code></td>
                <td>/api/v1/wallets/{WALLET_UUID}</td>
                <td>Получить баланс кошелька</td>
            </tr>
            <tr>
                <td><code>POST</code></td>
                <td>/api/v1/wallet</td>
                <td>Операции с кошельком (пополнение/списание)</td>
            </tr>
        </table>
        
        <h2>📥 Пример запроса</h2>
        <h3>GET /api/v1/wallets/{WALLET_UUID}</h3>
        <pre><code>
fetch("http://localhost:7777/api/v1/wallets/550e8400-e29b-41d4-a716-446655440000")
    .then(response => response.json())
    .then(data => console.log(data));
        </code></pre>
    </div>
</body>
</html>
