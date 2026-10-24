const express = require("express");

const authRoutes = require("./routes/authRoutes");

const app = express();
const PORT = 3001;

app.use(express.json());

app.use("/", authRoutes);

app.listen(PORT, () => {
  console.log(`Auth Service avviato sulla porta ${PORT}`);
});