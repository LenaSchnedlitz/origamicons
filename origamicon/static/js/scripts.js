// REFRESH FIXES //////////////////////////////////////////////////////////////

callOnFocus = () => {
  /*
  Compensates for missing onfocus call when using autofocus
   */
  const autofocused = document.activeElement;
  if (autofocused.onfocus) {
    autofocused.onfocus();
  }
};

moveCaretToInputEnd = (input) => {
  /*
  Refreshes input value to fix caret misplacement
   */
  const value = input.value;
  input.value = '';
  input.value = value;
};


// ORIGAMICON SETTER //////////////////////////////////////////////////////////

getLogoParams = () => {
  return {
    parentClass: 'logo',
    imageAlt: 'Logo',
    imageSrc: '../static/img/logo_origamicon.png'
  }
};

getOrigamiconParams = (origamiconText) => {
  return {
    parentClass: 'origamicon',
    imageAlt: `Origamicon for ${origamiconText}`,
    imageSrc: origamiconText,
    aDownload: `origamicon_${origamiconText}.png`,
    aHref: origamiconText
  }
};

show = (origamiconText) => {
  /*
  Shows an origamicon image for the given string
   */
  const data = origamiconText.trim() ?
    getOrigamiconParams(origamiconText) :
    getLogoParams();

  const parent = document.getElementById('container');
  parent.className = data.parentClass;

  const image = parent.getElementsByTagName('img')[0];
  image.alt = data.imageAlt;
  image.src = data.imageSrc;

  const a = parent.getElementsByTagName('a')[0];
  a.download = data.aDownload;
  a.href = data.aHref;
};
