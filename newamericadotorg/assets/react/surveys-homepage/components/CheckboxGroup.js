import { max } from 'moment';
import React from 'react';
import './CheckboxGroup.scss';

class CheckboxGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.props.options.forEach((val) => {
      this.state[val.id] = val.checked ? true : false;
    });
    this.handleChange = this.handleChange.bind(this);
    this.toggleCheckboxGroup = this.toggleCheckboxGroup.bind(this);
  }

  handleChange(e) {
    this.setState(
      {
        [e.target.id]: e.target.checked,
      },
      () => this.props.onChange(this.state)
    );
  }

  toggleCheckboxGroup() {
    console.log(27);
  }

  render() {
    const { options, title } = this.props;
    const isOpen = true;

    return (
      <div className="checkbox__container">
        <span
          className={`${
            isOpen ? 'margin-bottom-25' : ''
          } checkbox__group-title`}
          onClick={this.toggleCheckboxGroup}
        >
          {title}
          <i className={`fa fa-${isOpen ? 'times' : 'plus'}`}></i>
        </span>
        {isOpen &&
          options.map((option, i) => (
            <div className="checkbox-group__options" key={i}>
              <input
                id={option.id}
                type="checkbox"
                checked={this.state[option.id]}
                onChange={this.handleChange}
              />
              <label htmlFor={option.id} className="checkbox__label">
                {option.label}
              </label>
            </div>
          ))}
      </div>
    );
  }
}

export default CheckboxGroup;
