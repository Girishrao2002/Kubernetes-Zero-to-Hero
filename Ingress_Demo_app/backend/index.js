const express = require('express');
const Redis = require('ioredis');
const app = express();
const port = process.env.PORT || 4000;

const redisHost = process.env.REDIS_HOST || 'redis';
const redis = new Redis({ host: redisHost, port: 6379 });

app.get('/api/message', async (req, res) => {
  try {
    const key = 'visits';
    const visits = await redis.incr(key);
    res.json({ message: `Hello from backend — visit #${visits}` });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'error' });
  }
});

app.listen(port, () => console.log(`Backend listening on ${port}`));
