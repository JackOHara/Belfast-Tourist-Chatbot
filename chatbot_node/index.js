var restify = require('restify');
var builder = require('botbuilder');
var request = require('request');

//Create restify server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function () {
    console.log('%s listening to %s', server.name, server.url);
});

//Create bot
var connector = new builder.ChatConnector({
    appId: process.env.MICROSOFT_APP_ID,
    appPassword: process.env.MICROSOFT_APP_PASSWORD
});

var bot = new builder.UniversalBot(connector);

//Start server
server.post('/hello', connector.listen());

//Define bot behaviour
var bot = new builder.UniversalBot(connector, function (session) {
    var msg = session.message;
    //Checks if photo exists in message. Add validation to ensure attachment is photo.
    if (msg.attachments && msg.attachments.length > 0) {
        var attachment = msg.attachments[0];
        //Send image to flask. Flask returns stringified JSON.
        request.post({
            url: 'http://localhost:5000/predict',
            body: attachment.contentUrl
        }, function (r1, r2, body) {
            console.log("Message recieved from flask")
            processLocationInformation(body, session)
            //Make endDialog message dependent on result(whether it exists or not). Perhaps add another element to dictionary defining if result was successful.
            session.endDialog();
        });
    } else {
        var msg = 'Send me an image of a Belfast landmark!';
        session.endDialog(msg);
    }

    
    // if(msg.text.includes("language")){
    //     session.send("say what! language works")
    // }else{
    //     session.send("language aint working man")
    // }
});

//Stringified JSON is parsed and presented back to user through messages and cards.
//Add logic to deal with missing info in JSON
//Add scenario where a location is not found
function processLocationInformation(locationJSONString, session) {
    var locationInformation = JSON.parse(locationJSONString)
    var gmap_string1 = 'https://www.google.co.uk/maps/search/'
    var gmap_string2 = ',+'
    //https://www.google.co.uk/maps/search/54.593924,+-5.924265?sa=X&ved=0ahUKEwiOlo7xpZDaAhVbF8AKHRzPCwoQ8gEIKDAA
    var park = locationInformation["location"]["belfast_parks"]["NAME"]
    var park_gmap = gmap_string1 + locationInformation["location"]["belfast_parks"]["LATITUDE"] + gmap_string2 + locationInformation["location"]["belfast_parks"]["LONGITUDE"]
    var toilets = locationInformation["location"]["belfast_toilets"]["NAME"]
    var toilets_gmap = gmap_string1 + locationInformation["location"]["belfast_toilets"]["LATITUDE"] + gmap_string2 + locationInformation["location"]["belfast_parks"]["LONGITUDE"]
    var bikes = locationInformation["location"]["belfast_bikes"]["LOCATION"]
    var bikes_gmap = gmap_string1 + locationInformation["location"]["belfast_bikes"]["LATITUDE"] + gmap_string2 + locationInformation["location"]["belfast_parks"]["LONGITUDE"]
    var carpark = locationInformation["location"]["belfast_carparks"]["NAME"]
    var carpark_gmap = gmap_string1 + locationInformation["location"]["belfast_carparks"]["LATITUDE"] + gmap_string2 + locationInformation["location"]["belfast_parks"]["LONGITUDE"]

    
    var locationSummary = "The nearest bike station is " + locationInformation["location"]["belfast_bikes"]["LOCATION"] + '. [Directions](' + bikes_gmap + ') <br/>'
    locationSummary += "The nearest public toilet is " + locationInformation["location"]["belfast_toilets"]["NAME"] + '. [Directions](' + toilets_gmap + ') <br/>'
    locationSummary += "The nearest public park is " + locationInformation["location"]["belfast_parks"]["NAME"] + '. [Directions](' + park_gmap + ') <br/>'
    locationSummary += "The nearest car park is " + locationInformation["location"]["belfast_carparks"]["NAME"] + '. [Directions](' + carpark_gmap + ') <br/>'

    // session.send(locationInformation["wiki"]["page_title"])
    console.log(locationInformation)

    session.send(locationInformation["wiki"]["page_summary"])
    session.send(locationSummary);
}
