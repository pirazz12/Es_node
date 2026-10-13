const express = require("express");
const router = express.Router();
const {loginController} = require("../controllers/loginController"); // Importa il controller per gestire le richieste

    
// Definisce la route POST per ottenere le informazioni meteo di una città.
router.post("/login", loginController);

module.exports = router;