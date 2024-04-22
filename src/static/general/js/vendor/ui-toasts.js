// /**
//  * UI Toasts
//  */

// 'use strict';

// (function () {
//   // Bootstrap toasts example
//   // --------------------------------------------------------------------
//   const toastPlacementExample = document.querySelector('.toast-placement-ex'),
//     toastPlacementBtn = document.querySelector('#showToastPlacement');
//   let selectedType, selectedPlacement, toastPlacement;

//   // Dispose toast when open another
//   function toastDispose(toast) {
//     if (toast && toast._element !== null) {
//       if (toastPlacementExample) {
//         toastPlacementExample.classList.remove(selectedType);
//         DOMTokenList.prototype.remove.apply(toastPlacementExample.classList, selectedPlacement);
//       }
//       toast.dispose();
//     }
//   }
//   // Placement Button click
//   if (toastPlacementBtn) {
//     toastPlacementBtn.onclick = function () {
//       if (toastPlacement) {
//         toastDispose(toastPlacement);
//       }
//       selectedType = document.querySelector('#selectTypeOpt').value;
//       selectedPlacement = document.querySelector('#selectPlacement').value.split(' ');

//       toastPlacementExample.classList.add(selectedType);
//       DOMTokenList.prototype.add.apply(toastPlacementExample.classList, selectedPlacement);
//       toastPlacement = new bootstrap.Toast(toastPlacementExample);
//       toastPlacement.show();
//     };
//   }
// })();


/**
 * Show toasts function
 * @param {string} type (bg-primary, bg-secondary, etc.)
 * @param {string} placement Ubicación del toast (top-0 start-0, top-0 start-50 translate-middle-x, etc.)
 */
const placementMap = {
  'top-left': 'top-0 start-0',
  'top-center': 'top-0 start-50 translate-middle-x',
  'top-right': 'top-0 end-0',
  'middle-left': 'top-50 start-0 translate-middle-y',
  'middle-center': 'top-50 start-50 translate-middle',
  'middle-right': 'top-50 end-0 translate-middle-y',
  'bottom-left': 'bottom-0 start-0',
  'bottom-center': 'bottom-0 start-50 translate-middle-x',
  'bottom-right': 'bottom-0 end-0'
};
function showToast(type, placement, title, body) {
  const toastPlacementExample = document.querySelector('.toast-placement-ex');
  let selectedType, selectedPlacement, toastPlacement;

  // // Dispose toast when open another
  function toastDispose(toast) {
    if (toast && toast._element !== null) {
      if (toastPlacementExample) {
        toastPlacementExample.classList.remove(selectedType);
        DOMTokenList.prototype.remove.apply(toastPlacementExample.classList, selectedPlacement);
      }
      toast.dispose();
    }
  }

  // Show toast
  if (toastPlacementExample) {
    if(toastPlacement) {
      toastDispose(toastPlacement);
    }
    selectedType = 'bg-' + type;
    selectedPlacement = placementMap[placement].split(" ")

    console.log(selectedPlacement)

    $("#toast-title").text(title)
    $("#toast-body").text(body)
    toastPlacementExample.classList.add(selectedType);
    DOMTokenList.prototype.add.apply(toastPlacementExample.classList, selectedPlacement);
    toastPlacement = new bootstrap.Toast(toastPlacementExample);
    toastPlacement.show();
  }
}