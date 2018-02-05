import { Component } from 'react';
import CardMd from './CardMd';
import CardLg from './CardLg';
import { PromoMd } from './CardPromo';

export default class StoryGrid extends Component {
  state = {
    email: null
  }
  about(){
    let { program } = this.props;

    return (
      <PromoMd title="About" link={{ to: 'about', label: 'Read More'}}>
        <h2 className="margin-25">{program.description}</h2>
      </PromoMd>
    );
  }

  subscribe(){
    let { program } = this.props;
    return (
      <PromoMd title="Subscribe" link={{ to: `subscribe/?email=${this.state.email}`, label: 'Go'}}>
        <h2 className="margin-25">{`Be the first to hear about the latest events and research from ${program.name}`}</h2>
        <div className="input">
          <input type="text" value={this.state.email} required onChange={(e)=>{this.setState({email: e.target.value})}}/>
          <label className="input__label button--text">Email Address</label>
        </div>
      </PromoMd>
    );
  }
  cardMd = (index, size) =>{
    let { loaded, story_grid } = this.props;
    return ( <CardMd post={story_grid[index]} image_size={size} loaded={loaded} /> );
  }
  cols = () => {
    let { story_grid, program, loaded } = this.props;
    let cols = [[this.subscribe()], [], []];
    let items = story_grid.length;

    switch(items){
      case 2:
        cols[1] = cols[1].concat([
          this.cardMd(1, "square")
        ]);
        cols[2] = cols[2].concat([
          this.about()
        ]);
        break;
      case 3:
        cols[1] = cols[1].concat([
          this.cardMd(1, "square")
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(2, "landscape"),
          this.about()
        ]);
        break;
      case 4:
        cols[0] = cols[0].concat([
          this.cardMd(3, "square")
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.about()
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square")
        ]);
        break;
      case 5:
        cols[0] = cols[0].concat([
          this.cardMd(3, "landscape")
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.cardMd(4, "square")
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square"),
          this.about()
        ]);
        break;
      case 6:
        cols[0] = cols[0].concat([
          this.cardMd(3, "landscape"),
          this.cardMd(5, "landscape")
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.cardMd(4, "square")
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square"),
          this.about()
        ]);
        break;
      case 7:
        cols[0] = cols[0].concat([
          this.cardMd(3, "landscape"),
          this.cardMd(5, "square")
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.cardMd(4, "square"),
          this.cardMd(6, "square")
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square"),
          this.about()
        ]);
        break;
    }

    cols = cols.map((col,i)=>(
      <div className='col-lg-4'>
        {col}
      </div>
    ));

    return cols;
  }
  render(){
    let { story_grid, loaded } = this.props;
    if(story_grid.length===0){
      return (
        <div className="program__story-grid">
          <div className="row gutter-10">
            <div className="col-12">
              <h1 className="margin-top-60">We're just getting started! <br/>Check back soon.</h1>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="program__story-grid">
        <div className="row gutter-10">
          <div className="col-12">
            <CardLg post={story_grid[0]} loaded={loaded}/>
          </div>
          {this.cols()}
        </div>
      </div>
    );
  }
}
