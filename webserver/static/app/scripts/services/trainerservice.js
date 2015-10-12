'use strict';

angular.module('sbAdminApp')
  .service('trainerservice', function(serverComm) {


    this.startTraining = function(mid, pid, nepochs, curWeight){

      var query = {
        'type': 'start_training',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'nepochs': nepochs,
          'currentEpoch': curWeight,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };



    this.stopTraining = function(mid, pid){

      var query = {
        'type': 'stop_training',
        'params': {
          'modelId': mid,
          'paramsId': pid,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };

    this.attachHandler = function(mid, pid, callback){

      var ws = new WebSocket("ws://"+ location.host +"/trainersocket");

      ws.onopen = (function(){

        var query = {
          'type': 'attach_handler',
          'params': {
            'modelId': mid,
            'paramsId': pid,
            }
        };

          ws.send(JSON.stringify(query));
      });

      ws.onmessage = callback ;

    };


    this.get_epoch_list = function(mid, pid){

      var query = {
        'type': 'get_epoch_list',
        'params': {
          'modelId': mid,
          'paramsId': pid,
        }
      };

      var defer = serverComm.getData(query);
      return defer;


    };

    
    this.startEvaluation = function(mid, pid, did, curWeight, num){

      var query = {
        'type': 'start_evaluation',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'datasetId': did,
          'nsents': num,
          'currentEpoch': curWeight,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };    

    this.testSentance = function(mid, pid, sentance , curWeight){

      var query = {
        'type': 'test_sentance',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'sentance': sentance,
          'currentEpoch': curWeight,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };

    this.testSentancePrediction = function(mid, pid, sentance , curWeight){

      var query = {
        'type': 'test_sentance_prediction',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'sentance': sentance,
          'currentEpoch': curWeight,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };
    this.predictWordEmbedding = function(mid, pid, word , curWeight){

      var query = {
        'type': 'predict_word_embedding',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'word': word,
          'currentEpoch': curWeight,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };
    this.generate_sequence = function(mid, pid, curWeight){

      var query = {
        'type': 'generate_sequence',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'currentEpoch': curWeight,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };

  
});
