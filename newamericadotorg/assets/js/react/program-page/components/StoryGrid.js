import { Component } from 'react';
import CardMd from './CardMd';
import CardLg from './CardLg';
import { PromoMd } from './CardPromo';


const Mobile = (props) => (
  <div className="mobile-only">
    {props.children}
  </div>
);

export default class StoryGrid extends Component {
  state = {
    email: null,
  }
  about(force){
    let { program } = this.props;
    if(program.hide_subscription_card && !force) return null;
    return (
      <PromoMd key={`0-0`} title="About" link={{ to: 'about', label: 'Read More'}}>
        <h2 className="margin-25">{program.description}</h2>
      </PromoMd>
    );
  }

  subscribe(k=0){
    let { program } = this.props;
    let sub_text = program.subscription_card_text || `Be the first to hear about the latest events and research from ${program.name}`;
    return (
      <PromoMd key={`1-${k}`} title="Subscribe" link={{ to: `subscribe/?email=${this.state.email}`, label: 'Go'}}>
        <h2 className="margin-25">{sub_text}</h2>
        <div className="input">
          <input type="text" value={this.state.email||''} required onChange={(e)=>{this.setState({email: e.target.value})}}/>
          <label className="input__label button--text">Email Address</label>
        </div>
      </PromoMd>
    );
  }
  cardMd = (index, size, k=0) =>{
    let { loaded, story_grid } = this.props;
    return ( <CardMd post={story_grid[index]} key={`${index}-${k}`} image_size={size} loaded={loaded} /> );
  }
  cols = () => {
    let { story_grid, program, loaded } = this.props;
    let col0 = program.hide_subscription_card ? [this.about(true)] : [this.subscribe()];
    let cols = [col0, [], []];
    let items = story_grid.length;

    switch(items){
      case 2:
        cols[0] = cols[0].concat([
          <Mobile>{this.about(1)}</Mobile>
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(1, "square")
        ]);
        cols[2] = cols[2].concat([
          this.about()
        ]);
        break;
      case 3:
        cols[0] = cols[0].concat([
          <Mobile key={501}>{this.cardMd(1, "square")}</Mobile>
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(1, "square"),
          <Mobile key={500}>{this.about(1)}</Mobile>
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(2, "landscape"),
          this.about()
        ]);
        break;
      case 4:
        cols[0] = cols[0].concat([
          this.cardMd(3, "square"),
          <Mobile key={500}>{this.cardMd(1, "square", 1)}</Mobile>
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
          this.cardMd(3, "landscape"),
          <Mobile key={501}>{this.cardMd(1, "square", 1)}</Mobile>
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.cardMd(4, "square"),
          <Mobile key={500}>{this.about()}</Mobile>
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square"),
          this.about()
        ]);
        break;
      case 6:
        cols[0] = cols[0].concat([
          this.cardMd(3, "landscape"),
          this.cardMd(5, "landscape"),
          <Mobile key={501}>{this.cardMd(1, "square", 1)}</Mobile>
        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.cardMd(4, "square"),
          <Mobile key={500}>{this.about(1)}</Mobile>
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square"),
          this.about()
        ]);
        break;
      case 7:
        cols[0] = cols[0].concat([
          this.cardMd(3, "landscape"),
          this.cardMd(5, "square"),
          <Mobile key={501}>{this.cardMd(1, "square", 1)}</Mobile>

        ]);
        cols[1] = cols[1].concat([
          this.cardMd(2, "landscape"),
          this.cardMd(4, "square"),
          this.cardMd(6, "square"),
          <Mobile key={500}>{this.about(1)}</Mobile>
        ]);
        cols[2] = cols[2].concat([
          this.cardMd(1, "square"),
          this.about()
        ]);
        break;
    }

    cols = cols.map((col,i)=>(
      <div key={i} className={`col-md-6 col-lg-4 ${i==2 ? 'desktop-only' : ''}`}>
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
