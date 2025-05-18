console.log("linked?");

// Wait for DOM to load
document.addEventListener("DOMContentLoaded", function () {  
  // -------------------------------- uploading obj picture --------------------------------
  let objImg = document.querySelector(".obj-img img"); // get <img> in .material-img
  let uploadImgBtn = document.getElementById("uploadImg-btn");
  const uploadImg = document.getElementById("upload-img"); // file input
  let clearImg = document.querySelector(".clear-img input");
  let imgName = document.getElementById("img-name");
  const objType = objImg.getAttribute("alt").includes("material") ? "material" : "product";
  // console.log(`objtype: ${objType}`);

  uploadImgBtn.addEventListener("click", () => {
    uploadImg.click();
  })

  // when new image uploaded
  uploadImg.addEventListener("change", () => {
    getImgData();
  })

  function getImgData() {
    const file = uploadImg.files[0];
    if (file) {
      const fileReader = new FileReader();
      const fileName = file.name;

      // what to do when file successfully read
      fileReader.onload = function (e) {
        objImg.src = e.target.result;
        imgName.value = fileName;
        clearImg.checked = false;
      }

      // start reading selected file as data url
      fileReader.readAsDataURL(file);

      // reader.onload func muz be defined bfrhand
      // aft reader read file as data url, browser auto triggers the onload event
      // The load event of the FileReader interface is fired when a file has been read successfully
    }
  }

  // when clear image checked
  clearImg.addEventListener("change", function () {

    // default image but clearbox unchecked
    if (!this.checked && imgName.value === `${objType}_empty.jpeg`) {
      alert("Please select a new image or keep the clear option checked.");
      this.checked = true;
    }
    else {
      objImg.src = `/images/${objType}_empty.jpeg`;
      uploadImg.value = "";
      imgName.value = `${objType}_empty.jpeg`;
    }
  });


  // -------------------------------- adding product material --------------------------------
  // add materials for product
  const addMaterialBtn = document.getElementById("add-pm-btn");
  const deleteMaterialBtns = document.querySelectorAll(".delete-btn");
  let materialContainer = document.querySelector(".productmaterial-container");
  const materialBox = document.querySelector(".empty-box");

  // add material button
  if (addMaterialBtn && materialContainer && materialBox) {
    addMaterialBtn.addEventListener("click", event => {
      event.preventDefault(); // Prevent form submission on button click

      const newMaterialBox = materialBox.cloneNode(true);
      // true, node & subtree, including text in child Text nodes, oso copied
      // false, only the node cloned, subtree not cloned

      let deleteBtn = newMaterialBox.querySelector(".delete-btn");
      addDeleteListener(deleteBtn);

      newMaterialBox.style.display = "flex";
      newMaterialBox.classList.replace("empty-box", "productmaterial-box");

      // remove disabled attribute so views.py can read it as empty string if no option selected
      // dun remove disabled in hidden box to prevent views.py from reading it as well
      // instead remove here
      let selectedOption = newMaterialBox.querySelector("option");
      selectedOption.removeAttribute("disabled");

      // don't put name in hidden box cuz views.py will get hidden box's quantity too causing error
      // instead add it here
      let quantityInput = newMaterialBox.querySelector("input");
      quantityInput.name = "quantities_used";

      materialContainer.appendChild(newMaterialBox);
    });
  }
  else
    console.error("Unable to add new product material.");


  // delete material button
  if (deleteMaterialBtns) {
    deleteMaterialBtns.forEach(btn => {
      addDeleteListener(btn);
    })
  }
  else
    console.error("Delete material button not found.");

  function addDeleteListener(btn) {
    btn.addEventListener("click", event => {
      event.preventDefault();

      const parent = btn.parentElement;
      if (parent) {
        console.log(parent);
        parent.remove();
      }
      else
        console.error("Unable to remove this product material.");
    })
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

  // 

  // -------------------------------- submitting form --------------------------------
  // const form = document.querySelector("form");
  // const saveBtn = document.getElementById('save-btn');

  // form.addEventListener("submit", event => {
  //   event.preventDefault();

  // })

  // cancel button
  const cancelBtn = document.getElementById("cancel-btn");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      // location.href = cancelBtn.getAttribute("data-url"); // dun use 'this', 'this' is document
      history.back();
    })
  }

  // save button
  // let saveBtn = document.getElementById("save-btn");
  // if (saveBtn) {
  //   saveBtn.addEventListener("click", function () {
  //     document.querySelector("form").submit();
  //   });
  // }

});

