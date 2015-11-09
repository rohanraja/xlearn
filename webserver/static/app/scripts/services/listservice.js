'use strict';

angular.module('sbAdminApp')
  .service('listservice', function(serverComm) {


    this.loadDatasets = function(){

      var query = {
        'type': 'loadDatasets',
        'params': {
        }
      };

      var defer = serverComm.getData(query);

      return defer ;
    };

    this.datasetList = function($modelid){

      var query = {
        'type': 'dataset_list',
        'params': {
        }
      };

      var defer = serverComm.getData(query);

      return defer ;

    };

    this.loadMappers = function($modelid){

      var query = {
        'type': 'mappers_list',
        'params': {
        }
      };

      var defer = serverComm.getData(query);

      return defer ;

    };


    this.loadEmbeddings = function($modelid){

      var query = {
        'type': 'embeddings_list',
        'params': {
        }
      };

      var defer = serverComm.getData(query);

      return defer ;

    };

    this.loadModels = function($modelid){
      var query = {
        'type': 'models_list',
        'params': {
        }
      };

      var defer = serverComm.getData(query);

      return defer ;
    };

  
    this.getMapperStats = function($modelid){
      var query = {
        'type': 'get_mapper_stats',
        'params': {
          "modelId": $modelid
        }
      };

      var defer = serverComm.getData(query);

      return defer ;
    };

  
    this.getSearchPhrase = function($modelid, phrase){
      var query = {
        'type': 'search_dataset',
        'params': {
          "modelId": $modelid,
          "phrase": phrase,
        }
      };

      var defer = serverComm.getData(query);

      return defer ;
    };

    this.deleteParam = function($modelid, $paramid){
      var query = {
        'type': 'delete_param',
        'params': {
          "modelId": $modelid,
          "paramsId": $paramid,
        }
      };

      var defer = serverComm.getData(query);

      return defer ;
    };

  });
