import { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Heading extends Component {

  render(){
    let { program } = this.props;

    return (
      <div className="program__header container margin-bottom-10">
  			<div className="program__heading__wrapper">
  					<h1 className="margin-0 promo"><Link to={program.url}>{program.name}</Link></h1>
  			</div>
  		</div>
    );
  }
}
