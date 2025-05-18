console.log("linked?");

let addMaterialBtn = document.getElementById("addMaterialBtn");
let materialContainer = document.getElementById("materials-container");
// let currentMaterialBox = materialContainer.getElementsByClassName(".material-box")
// let deleteBtn = document.getElementById("deleteBtn");

//add
if (addMaterialBtn && materialContainer) {
  addMaterialBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent form submission on button click

    //clone the 1st material box
    const newMaterialBox = document.querySelector(".material-box").cloneNode(true);
    //true, node & subtree, including text in child Text nodes, oso copied
    //false, only the node cloned, subtree not cloned

    //clear the values in cloned box for new input
    newMaterialBox.querySelector('select[name="materials"]').selectedIndex = 0; //select 1st option(empty option), -1 deselects everything but not every browser supports
    newMaterialBox.querySelector('input[name="quantities_used"]').value = "";

    //append new box to material-container
    materialContainer.appendChild(newMaterialBox);
    //cloned node has no parent & not part of document
    //until it is added to another node that is part of the document
    //using Node.appendChild() or a similar method
  });


  //delete
  // deleteBtn.addEventListener("click", function (event) {
  //   event.preventDefault();
  //   console.log("dlt");
  //   const materialBox = event.target.closest(".material-box");
  //   materialBox.remove();

  // });

  // console.log(materialContainer);

  materialContainer.addEventListener("click", function (event) {
    // console.log('2222222');
    console.log(event.target.className);
    if (event.target.classList.contains("deleteBtn")) {
      // console.log('3333333333');
      event.preventDefault();
    
      // console.log("dlt");
      let materialBox = event.target.closest(".material-box");

      if (materialBox) {
        // console.log("deleteeeeee");
        materialBox.remove();
      }
      else {
        console.log("error");
      }
    
    }
    else {
      console.log("not deleted");
    }
    console.log("nothing happened");
  });
}

/*
event = obj auto passed to event handler func when an event is triggered (e.g a click)
target = returns element tht triggered the event (e.g the button clicked)
*currentTarget = returns element whose event listener triggered the event

classList = read-only, list of class names of target element
*An element can hv multiple class names, common in web development to apply multiple styles/functionalities to an element 
 Each class name is separated by a space: <div class="button deleteBtn highlighted"></div>

contains = Returns true if the list contains a class
closest = starts at d element itself, den ancestors (parent, grandparent) until a match is found, or null
*/
