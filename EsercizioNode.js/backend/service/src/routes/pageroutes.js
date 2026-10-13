//raccolgo qui tutte le routes delle pages, ossia i percorsi utili per gestire l'invio delle pagine statiche
//in altri termini tutti i get saranno raccolti qui

const express = require("express");
const router = express.Router();
const path = require("path");

router.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "../../../../frontend/public/index.html"));
});

router.get("/login", (req, res) => {
    res.sendFile(path.join(__dirname, "../../../../frontend/public/login.html"));
});

router.get("/about", (req, res) => {
    res.sendFile(path.join(__dirname, "../../../../frontend/public/about.html"));
});

router.get("/signup", (req, res) => {
    res.sendFile(path.join(__dirname, "../../../../frontend/public/signup.html"));
});

router.get("/weather", (req, res) => {
    res.sendFile(path.join(__dirname, "../../../../frontend/public/weather.html"));
});

router.get("/contact", (req, res) => {
    res.sendFile(path.join(__dirname, "../../../../frontend/public/contact.html"));
});

module.exports = router;
