document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  
    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {
  
        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
  
      });
    });
  
});

function findObjectByName(jsonArray, name) {
  for(var i = 0; i < jsonArray.length; i++) {
    if(jsonArray[i].name == name) {
      return jsonArray[i];
    }
  }
  return null;
}

document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('click', (e) => {
      e.preventDefault();
      selectedLang = e.currentTarget.getAttribute('id');
      fetch('/api/getlanguages')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(jsonArray => {
          let jsonObj = findObjectByName(jsonArray, selectedLang);
          if (jsonObj && jsonObj['greeting']) {
            greeting = jsonObj['greeting'];
            greeting = greeting.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
            document.getElementById("consoleBox").innerHTML = greeting;
          }
        })
        .catch(error => console.log('There was an error: ', error));
  });
});
