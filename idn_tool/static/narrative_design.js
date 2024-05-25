function changeBorder(colId) {
  // Reset border for all columns
  document.querySelectorAll('.col-edit-node').forEach(col => {
    col.classList.remove('border-highlight');

  });

  // Remove close button from all columns
  document.querySelectorAll('.close-btn').forEach(btn => {
    btn.remove();
  });


  // Highlight the clicked column
  document.getElementById(colId).classList.add('border-highlight');
  // If the column is highlighted, add a close button
  if (document.getElementById(colId).classList.contains('border-highlight')) {
    const closeButton = document.createElement('span');
    closeButton.innerHTML = '&times;'; // Unicode for '×' (close symbol)
    closeButton.classList.add('close-btn');
    closeButton.onclick = function(event) {
      event.stopPropagation(); // Prevents the click event from bubbling up to the column
      document.getElementById(colId).classList.remove('border-highlight');
      this.remove(); // Remove the close button
    };
    document.getElementById(colId).appendChild(closeButton);
  }

}



