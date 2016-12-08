/**
* Authentication
* @namespace thinkster.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('thinkster.authentication.services')
    .factory('ShareVar',ShareVar);

  function ShareVar(){
  	var irs = {};

  	function setRValue(value){
  		angular.copy(value,irs)
  	}

  	var shareVar = {
  		setRValue: setRValue,
  		isRegisterSuccess: irs
  	};
  	
  	return shareVar;
  };
})()