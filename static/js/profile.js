document.addEventListener("DOMContentLoaded", () => {
    
    // -------------------------------- uploading pfp --------------------------------
    let pfpImg = document.querySelector(".profile-pic img");
    let uploadPfpBtn = document.getElementById("uploadPfp-btn");
    const uploadPfp = document.getElementById("upload-pfp"); // file input
    let clearPfp = document.querySelector(".clear-pfp input");
    let pfpName = document.getElementById("pfp-name");

    uploadPfpBtn.addEventListener("click", e => {
        e.preventDefault();
        uploadPfp.click();
    })

    // when new pfp uploaded
    uploadPfp.addEventListener("change", () => {
        getPfpData();
    })

    function getPfpData() {
        const file = uploadPfp.files[0];
        if (file) {
            const fileReader = new FileReader();
            const fileName = file.name;

            // what to do when file successfully read
            fileReader.onload = function (e) {
                pfpImg.src = e.target.result;
                pfpName.value = fileName;
                clearPfp.checked = false;
            }

            // start reading selected file as data url
            fileReader.readAsDataURL(file);

            // reader.onload func muz be defined bfrhand
            // aft reader read file as data url, browser auto triggers the onload event
            // The load event of the FileReader interface is fired when a file has been read successfully
        }
    }

    // when clear image checked
    clearPfp.addEventListener("change", function () {

        // default image but clearbox unchecked
        if (!this.checked && pfpName.value === `user.png`) {
            alert("Please select a new profile picture or keep the clear option checked.");
            this.checked = true;
        }
        else {
            pfpImg.src = `/images/user.png`;
            uploadPfp.value = "";
            pfpName.value = `user.png`;
        }
    });

    const cancelBtn = document.getElementById("cancel-btn");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", () => {
            // location.href = cancelBtn.getAttribute("data-url"); // dun use 'this', 'this' is document
            history.back();
        })
    }
});