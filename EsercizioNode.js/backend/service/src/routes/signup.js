const express = require("express");
const router = express.Router();
const {signupController} = require("../controllers/signupController"); // Importa il controller per gestire le richieste

    
// Definisce la route POST per ottenere le informazioni meteo di una città.
router.post("/signup", signupController);

module.exports = router;