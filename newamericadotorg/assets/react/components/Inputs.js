import React from 'react';

export const RadioButton = (props) => (
  <div className="inline checkbox checkbox--radio-button">
    <label htmlFor={props.name} className="margin-0 h6 checkbox__label">
      {props.label}
    </label>
    <input className="checkbox__input" type="radio" {...props} />
    <div className="checkbox__indicator"></div>
  </div>
);

export const CheckBox = (props) => (
  <div className="checkbox checkbox--checkbox">
    <label htmlFor={props.name} className="margin-0 h6 checkbox__label">
      {props.label}
    </label>
    <input className="checkbox__input" type="checkbox" {...props} />
    <div className="checkbox__indicator"></div>
  </div>
);

export const Text = ({ children, ...props}) => (
  <div className="input">
    <input type="text" {...props} />
    <label className="input__label" htmlFor={props.name}>
      <h5 className="margin-0">
        {props.label}
        {props.required && (
           <span aria-label="required" class="required-asterisk"> *</span>
         )}
      </h5>
    </label>
    {children}
  </div>
);

Text.defaultProps = {
  required: true,
}

export const TextArea = ({ children, ...props}) => (
  <div className="input">
    <textarea type="text" rows="4" required {...props} />
    <label className="input__label" htmlFor={props.name}>
      <h5 className="margin-0">{props.label}</h5>
    </label>
    {children}
  </div>
);
