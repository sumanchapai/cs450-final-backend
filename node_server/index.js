const express = require("express");
const cors = require("cors");

const redis = require("redis");

// Redis settings
const client = redis.createClient();
const tempKey = "temp-cs-450";

const app = express();
// Allow CORS
app.use(cors());

// Server settings
const hostname = "0.0.0.0";
const port = 3000;

client.on("error", (err) => console.log("Redis Client Error", err));

client
    .connect()
    .then((x) => {
        app.get("/", async (req, res) => {
            res.setHeader("Content-Type", "application/json");
            try {
                const tempValue = await client.HGETALL(tempKey);
                const msg = JSON.stringify({ value: tempValue });
                res.statusCode = 200;
                res.end(msg);
            } catch (e) {
                console.log(e);
                const msg = JSON.stringify({ error: e });
                res.statusCode = 400;
                res.end(msg);
            }
        });
    })
    .catch((e) => {
        console.log("error", e);
    });

app.listen(port, hostname, () => {
    console.log(`server is listening on port ${hostname}:${port}`);
});

