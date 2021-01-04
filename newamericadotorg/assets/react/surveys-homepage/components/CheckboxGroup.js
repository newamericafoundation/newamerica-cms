import React from 'react';
import { PlusX } from '../../components/Icons';
import './CheckboxGroup.scss';

class CheckboxGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
    };

    this.props.options.forEach((val) => {
      this.state[val.id] = val.checked ? true : false;
    });
  }

  handleChange = (e) => {
    this.setState(
      {
        [e.target.id]: e.target.checked,
      },
      () => this.props.onChange(this.state)
    );
  };

  toggleCheckboxGroup = () => {
    this.setState({ isOpen: !this.state.isOpen });
  };

  render() {
    const { isOpen } = this.state;
    const { options, title } = this.props;
    const _options = options
      .filter((item) => {
        return item.id !== 'isOpen';
      })
      .sort((a, b) => {
        return a.label.localeCompare(b.label);
      });

    return (
      <div
        className={`checkbox-group ${
          isOpen && 'checkbox-group--is-open'
        }`}
      >
        <span
          className={`${
            isOpen ? 'margin-bottom-25' : ''
          } checkbox-group__title`}
          onClick={this.toggleCheckboxGroup}
        >
          {title}

          <div className="icon">
            <PlusX x={isOpen} />
          </div>
        </span>
        <div
          className={`checkbox-group__options ${
            isOpen ? 'is-open' : ''
          }`}
        >
          {_options.map((option, i) => (
            <div className="checkbox-group__option" key={i}>
              <input
                id={option.id}
                type="checkbox"
                checked={this.state[option.id]}
                onChange={this.handleChange}
              />
              <label
                htmlFor={option.id}
                className="checkbox-group__label"
              >
                {option.label}
              </label>
            </div>
          ))}
        </div>
      </div>
    );
  }
}

export default CheckboxGroup;
