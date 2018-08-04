import './Panel.scss';

import React, { Component } from 'react';

export default class Panel extends Component {
  parseHTMLText = (html) => {
    let div = document.createElement('div');
    div.innerHTML = html;
    return div.innerText;
  }
}
