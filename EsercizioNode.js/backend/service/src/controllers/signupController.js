
exports.signupController = async (req, res) => {

    app.post('/signup', (req, res) => {             // Definisce la route POST per elaborare la registrazione.
        const { username, password } = req.body;      // Estrae username e password dal corpo della richiesta.
        res.send('Registrazione completata per: ' + username); // Risponde confermando la registrazione.
    });// Chiude la route POST /login.
};

// qua metto la logica di manipolazione dei dati