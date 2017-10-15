// dependencies
var restify = require('restify');
var builder = require('botbuilder');
var request = require('request'); // npm install

// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function () {
   console.log('%s listening to %s', server.name, server.url); 
});


// Create chat connector for communicating with the Bot Framework Service
var connector = new builder.ChatConnector({
    appId: process.env.MICROSOFT_APP_ID,
    appPassword: process.env.MICROSOFT_APP_PASSWORD
});

// create the bot
var bot = new builder.UniversalBot(connector);

// Listen for messages from users 
server.post('/botB', connector.listen());

//entry point for branches and receving an image
var bot = new builder.UniversalBot(connector, function(session){

});


bot.dialog('A', [
	function (session) {

    },
    function (session, results) {

    }
]).triggerAction({
    matches: /^a$/i
});



bot.dialog('B', [
    function (session) {

    },
    function (session, results) {

    }
]).triggerAction({
    matches: /^b$/i
});


bot.dialog('C', [
    function (session) {
 
    },
    function (session, results) {

    }
]).triggerAction({
    matches: /^c$/i
});

bot.dialog('D', [
    function (session) {

    },
    function (session, results) {

    }
]).triggerAction({
    matches: /^d$/i
});
