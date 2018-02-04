import { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Heading extends Component {

  render(){
    let { program } = this.props;

    return (
      <div className="program__header margin-bottom-10">
  			<div className="program__heading__wrapper">
  					<h1 className="margin-0 promo">
              {program.parent_programs &&
                <label className="block margin-top-0 margin-bottom-15 with-caret--left">
                  <a href={program.parent_programs[0].url}>
                    {program.parent_programs[0].name}
                  </a>
                </label>}
              <Link to={program.url}>{program.name}</Link>
            </h1>
  			</div>
  		</div>
    );
  }
}
