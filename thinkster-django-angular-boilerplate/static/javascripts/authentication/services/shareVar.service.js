/**
* Authentication
* @namespace thinkster.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('thinkster.authentication.services')
    .factory('ShareVar',ShareVar);

  ShareVar.$inject = ['$http'];

  function ShareVar($http){

  	var ShareVar = {
      search_books:search_books
  	};
  	
  	return ShareVar;

    function search_books(author,publisher,bk_title,subject) {
      return $http.post('/search/',{
        author: author,
        publisher: publisher,
        bk_title: bk_title,
        subject: subject
      }).then(searchSuccessFn, searchErrorFn);

      function searchSuccessFn(data, status, headers, config) {
        console.log("success")

        window.location = '/search';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function searchErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }
  };
})()