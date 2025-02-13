/********************************************************************************
*  WEB422 – Assignment 2
* 
*  I declare that this assignment is my own work in accordance with Seneca's
*  Academic Integrity Policy:
* 
*  https://www.senecapolytechnic.ca/about/policies/academic-integrity-policy.html
* 
*  Name: _Harnoor Kaur Dran_ Student ID: 145433223 Date: 26 Jan, 2025
*
********************************************************************************/



document.addEventListener("DOMContentLoaded", function()
{
  let page = 1;
  const perPage = 10;
  let searchName = null;


  // Pull listing data from your published listing APIs
  // Adding click events to row item and populate a modal window.
  function loadListingsData()
  {
    let URL = `https://listings-api-ud7m.vercel.app/api/listings?page=${page}&perPage=${perPage}`;

    if(searchName){
      URL += `&name=${encodeURIComponent(searchName)}`;
    }
  
    fetch(URL)      

      .then(function(res) {
        if (res.ok) {
          return res.json();
        }
        throw new Error(`Failed to fetch data: ${res.status}`);
      })
      .then(data => {
        if(data.length){
          const tableBody = document.querySelector("#listingsTable tbody");
          tableBody.innerHTML = data.map(listing => {
            return `
              <tr data-id="${listing._id}">
                <td>${listing.name}</td>
                <td>${listing.room_type}</td>
                <td>${listing.address.street}, ${listing.address.city}, ${listing.address.country}</td>
                <td>
                    ${listing.summary || ''}
                    <br><br>
                    <strong>Accommodates:</strong> ${listing.accommodates}
                    <br>
                    <strong>Rating:</strong> ${listing.review_scores ? listing.review_scores.review_scores_rating : 'N/A'} (${listing.number_of_reviews} Reviews)
                </td>
            </tr>
        `;
    }).join("");
  
    document.querySelector("#current-page").textContent = page;

    document.querySelectorAll("#listingsTable tbody tr").forEach(row => {
      row.addEventListener("click",function() {
        const listingId = this.getAttribute("data-id");

        fetch(`https://listings-api-ud7m.vercel.app/api/listings/${listingId}`)
        .then(res => res.json())
        .then(listingDetails => {
            // Populate the modal with listing details
            const modalBody = document.querySelector("#detailsModal .modal-body");
            modalBody.innerHTML = `
                <img id="photo" onerror="this.onerror=null;this.src = 'https://placehold.co/600x400?text=Photo+Not+Available'" class="img-fluid w-100" src="${listingDetails.images.picture_url || 'https://placehold.co/600x400?text=Photo+Not+Available'}">
                <br><br>
                ${listingDetails.neighborhood_overview || ''}
                <br><br>
                <strong>Price:</strong> ${listingDetails.price.toFixed(2)}
                <br>
                <strong>Room:</strong> ${listingDetails.room_type}
                <br>
                <strong>Bed:</strong> ${listingDetails.bed_type} (${listingDetails.beds} beds)
            `;
            $('#detailsModal').modal('show');
        });
      });
      });
      document.querySelector("#current-page").textContent = page;
  

      } else 
      {
        if (page > 1) {
          page--;
          loadListingsData();
          }
        
        else{
        const tableBody = document.querySelector("#listingsTable tbody");
        tableBody.innerHTML = `
        <tr><td colspan="4"><strong>No data available</strong></td></tr>
        `;
      
      }}
      
      })
      .catch(err => {
      console.error("Error fetching data: ", err);
      const tableBody = document.querySelector("#listingsTable tbody");
      tableBody.innerHTML = `
      <tr><td colspan="4"><strong>No data available</strong></td></tr>
      `;
      });
    }

      // Click event for the "previous page" button
      document.getElementById("previous-page").addEventListener("click", function () {
      if (page > 1) {
      page--;
      loadListingsData();
      }
      });

      // Click event for the "next page" button
      document.getElementById("next-page").addEventListener("click", function () {
      page++;
      loadListingsData();
      });

      // Submit event for the search form
      document.getElementById("searchForm").addEventListener("submit", function (e) {
      e.preventDefault();
      searchName = document.getElementById("search-name").value;
      page = 1; // Reset to the first page
      loadListingsData();
      });

      // Click event for the "clear" button
      document.getElementById("clearForm").addEventListener("click", function () {
      document.getElementById("search-name").value = "";
      searchName = null;
    
      loadListingsData();
      });
          
    loadListingsData();

});


