document.addEventListener("DOMContentLoaded", function () {
    // -------------------------------- taskbar --------------------------------
    // Set dashboard as active by default
    document.getElementById("dash-btn").classList.add("active");

    // Taskbar active states
    const taskbarButtons = document.querySelectorAll(".taskbar button");

    taskbarButtons.forEach((button) => {
        button.addEventListener("click", function () {
            console.log("taskbar btn listener");
            // Remove active class from all buttons
            taskbarButtons.forEach((btn) => {
                btn.classList.remove("active");
            });

            // Add active class to clicked button
            this.classList.add("active");
        });
    });

    // -------------------------------- filter --------------------------------
    const filterBtn = document.getElementById("filter-btn");
    const materialFilters = document.querySelector(".material-filters");
    const productFilters = document.querySelector(".product-filters");

    // === toggle filter === 
    filterBtn.addEventListener("click", function () {
        console.log("filter btn listener");
        materialFilters.classList.toggle("active");
        productFilters.classList.toggle("active");

        // // Toggle active state on filter button
        // this.classList.toggle("active");
        // console.log("filter btn active");
    });

    // const materialFilterForm = document.getElementById("material-filter-form");
    
    const Mfilters = materialFilters.querySelectorAll("select");
    const Pfilter = productFilters.querySelector("select");
    const params = new URLSearchParams(window.location.search);
    

    // === initialise filter ===
    // open filter
    if (params.size !== 0) {
        // taskbarButtons.forEach(btn => {
        //   console.log(btn);
        //   if (btn === filterBtn)
        //     console.log("sameeeee");
        //   btn.classList.remove("active");
        // });
        console.log(params.toString());

        filterBtn.click();
    }

    // initialise material filter
    Mfilters.forEach(filter => {
        const MparamValue = params.get(filter.name);
        if (MparamValue) {
            for (option of filter.options) {
                if (option.value === MparamValue) {
                    option.selected = true;
                    break;
                }
            }
        }
    })

    // initialise product filter
    const PparamValue = params.get(Pfilter.name);
    if (PparamValue) {
        for (option of Pfilter.options) {
            if (option.value === PparamValue) {
                option.selected = true;
                break;
            }
        }
    }

    // === filtering ===
    // material filter
    Mfilters.forEach(filter => {
        filter.addEventListener("change", filterMaterials);
    })

    function filterMaterials() {
        Mfilters.forEach(filter => {
            if (filter.value !== "")
                params.set(filter.name, filter.value);
            else
                params.delete(filter.name);
        })

        const url = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
        window.location.href = url;
        // history.pushState({}, '', url); // change the URL, and keep the old one in the browser history
    }

    // product filter
    Pfilter.addEventListener("change", () => {
        console.log("enter listener");
        if (Pfilter.value !== "")
            params.set(Pfilter.name, Pfilter.value);
        else
            params.delete(Pfilter.name);

        const url = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
        window.location.href = url;
    })


    // === reset button ===
    const materialResetBtn = materialFilters.querySelector(".reset");
    const productResetBtn = productFilters.querySelector(".reset");

    materialResetBtn.addEventListener("click", function () {
        // Reset is handled by the browser for type="reset"
        // This just provides feedback
        params.delete("mcat");
        params.delete("col");
        params.delete("supp");

        // window.location.href = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
        history.pushState({}, '', window.location.pathname);
    });

    productResetBtn.addEventListener("click", function () {
        params.delete("pcat");

        // window.location.href = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
        history.pushState({}, '', window.location.pathname);
    });

    // -------------------------------- add buttons --------------------------------
    const addNewMaterial = document.getElementById("add-material-btn");
    if (addNewMaterial) {
        addNewMaterial.addEventListener("click", function () {
            location.href = "/add-material/"; //the 1st '/' means absolute path, w/o it the add-material/ will b appended to adminn/
        });
    }

    const addNewProduct = document.getElementById("add-product-btn");
    if (addNewProduct) {
        addNewProduct.addEventListener("click", function () {
            location.href = "/add-product/"; //the 1st '/' means absolute path, w/o it the add-material/ will b appended to adminn/
        });
    }

    // -------------------------------- manage buttons --------------------------------
    const manageButtons = document.querySelectorAll(".manage-btn");

    manageButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            // Prevent event bubbling
            event.stopPropagation();

            let manageDropdown = button.nextElementSibling;
            // console.log(manageDropdown);
            manageDropdown.classList.toggle("active");
        });
    });

    /*
    // -------------------------------- edit buttons --------------------------------
    const editBtns = document.querySelectorAll(".edit-btn");
    if (editBtns) {
      editBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          location.href = btn.getAttribute("data-url");
        })
      });
    }
    */

    /*
    // -------------------------------- delete buttons --------------------------------
    const deleteBtns = document.querySelectorAll(".delete-btn");
    if (editBtns) {
      editBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          location.href = btn.getAttribute("data-url");
        })
      });
    }
    */

    // mcm no use....
    // -------------------------------- cards --------------------------------
    const materialCards = document.querySelectorAll(".material-card");
    const productCards = document.querySelectorAll(".product-card");

    function makeCardsClickable(cards) {
        cards.forEach((card) => {
            card.addEventListener("click", function () {

                //*= means all tht contains 'admin-material', select the 1st one (queryselector)
                // select the 1st <a> tht has this
                const link = card.querySelector("a[href *= 'admin-material']") ?
                    card.querySelector("a[href *= 'admin-material']") :
                    card.querySelector("a[href *= 'admin-product']");
                //haven include productsssss???
                if (link)
                    location.href = link.getAttribute("href"); // get attr href in selected a
            });
        });
    };

    makeCardsClickable(materialCards);
    makeCardsClickable(productCards);

});