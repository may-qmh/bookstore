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
      search_books:search_books,
      get_book_info:get_book_info
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

    function get_book_info(isbn10) {
      return $http.post('/book/'+isbn10,{
        isbn10: isbn10
      }).then(searchSuccessFn, searchErrorFn);

      function searchSuccessFn(data, status, headers, config) {
        console.log("success")

        window.location = '/book/'+isbn10;
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