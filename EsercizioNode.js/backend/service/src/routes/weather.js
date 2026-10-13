const express = require("express");
const router = express.Router();
const {weatherController} = require("../controllers/weathercontroller"); // Importa il controller per gestire le richieste meteo.

    
// Definisce la route POST per ottenere le informazioni meteo di una città.
router.post("/weather", weatherController);

module.exports = router;