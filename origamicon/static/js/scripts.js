// REFRESH FIXES //////////////////////////////////////////////////////////////

/**
 * Compensates for missing onfocus call when using autofocus
 */
callOnFocus = () => {
  const autofocused = document.activeElement;
  if (autofocused.onfocus) {
    autofocused.onfocus();
  }
};

/**
 * Refreshes input value to fix caret misplacement
 */
moveCaretToInputEnd = (input) => {
  const value = input.value;
  input.value = '';
  input.value = value;
};

// ORIGAMICON SETTER //////////////////////////////////////////////////////////

getLogoParams = () => {
  return {
    parentClass: 'logo',
    imageAlt: 'Logo',
    imageSrc: '../static/img/logo_origamicon.png',
  };
};

getOrigamiconParams = (origamiconText) => {
  return {
    parentClass: 'origamicon',
    imageAlt: `Origamicon for ${origamiconText}`,
    imageSrc: origamiconText,
    aDownload: `origamicon_${origamiconText}.png`,
    aHref: origamiconText,
  };
};

/**
 * Displays the origamicon for the given text.
 *
 * If no text is given, renders the origamicon logo instead.
 */
showOrigamicon = (origamiconText) => {
  const data = origamiconText.trim()
    ? getOrigamiconParams(origamiconText)
    : getLogoParams();

  const parent = document.getElementById('picture');
  parent.className = data.parentClass;

  const image = parent.getElementsByTagName('img')[0];
  image.alt = data.imageAlt;
  image.src = data.imageSrc;

  const a = parent.getElementsByTagName('a')[0];
  a.download = data.aDownload;
  a.href = data.aHref;
};

/**
 * Renders a new origamicon if the input value does not change for 0.6s.
 */
refreshOrigamicon = (input) => {
  const old_value = input.value;
  setTimeout(() => {
    const new_value = input.value;
    if (old_value === new_value) {
      showOrigamicon(new_value);
    }
  }, 600);
};
