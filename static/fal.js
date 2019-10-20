"use strict";

function Showpoem(response) {
     // Remember, you can use console.dir to debug!
  console.dir(response);
  console.log('this is in `response`:');
  // console.log(response);
  // Display response from the server
  console.log($(response.e_beit));
  console.log($(response.f_beit));
}

http://localhost:5000/poem?$('#myBtn').on('submit', $('#respond').load(Showpoem);