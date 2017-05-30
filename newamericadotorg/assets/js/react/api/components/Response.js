import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { mapStateToProps, mapDispatchToProps } from './Fetch';

class Response extends Component {
  static propTypes = {
    name: PropTypes.string.isRequired,
    component: PropTypes.oneOfType([
      PropTypes.func,
      PropTypes.string
    ])
  }

  static defaultProps = {
    component: 'span'
  }

  render(){
    let { children, className } = this.props;
    return (
      <this.props.component {...this.props} className={'compose__response-component ' + (className||'')}>
        {children}
      </this.props.component>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Response);
