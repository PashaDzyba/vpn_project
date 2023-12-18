// main.js

document.addEventListener('DOMContentLoaded', function() {

  // Code for home.html
  if (document.querySelector('.home-page')) {
    console.log('Home page specific JavaScript here');
  }

  // Code for server_list.html
  if (document.querySelector('.server-list-page')) {
    console.log('Server list page specific JavaScript here');
    document.querySelectorAll('.server-item').forEach(function(item) {
      item.addEventListener('click', function() {
        alert('Server clicked: ' + this.textContent.trim());
      });
    });
  }

  // Code for connection_logs.html
  if (document.querySelector('.connection-logs-page')) {
    console.log('Connection logs page specific JavaScript here');
    document.querySelectorAll('.log-timestamp').forEach(function(timestamp) {
      timestamp.textContent = formatDate(timestamp.textContent);
    });
  }
});

function formatDate(dateString) {
  let date = new Date(dateString);
  return date.toLocaleString();
}

// Additional check to ensure Bootstrap components are initialized
$(function() {
  // Initialize all tooltips
  $('[data-toggle="tooltip"]').tooltip();

  // Initialize all popovers
  $('[data-toggle="popover"]').popover();

  // Initialize all dropdowns (if not automatically initialized)
  $('.dropdown-toggle').dropdown();
});
