
export const Arrow = ({ direction, ...props }) => (
  <div className={`icon-arrow ${direction}`} {...props}>
    <div />
    <div />
    <div />
  </div>
);

export const Doc = (props) => (
  <div className={`icon-doc`} {...props}>
    <div />
    <div />
    <div />
    <div />
    <div />
  </div>
);

export const PlusX = ({x, white, ...props}) => (
  <div className={`icon-plus${x ? ' x' : ''}${white ? ' white' : ''}`} {...props}>
    <div />
    <div />
  </div>
);
