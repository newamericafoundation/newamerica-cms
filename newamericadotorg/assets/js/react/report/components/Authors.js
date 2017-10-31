const Authors = ({ authors }) => (
  <div className="report__authors">
    <div className="report__authors__desktop">
    <label className="block bold bottom-margin">Authors</label>
    {authors.map((a)=>(
      <div className="report__authors__item">
        <label className="block">{`${a.first_name} ${a.last_name}`}</label>
        <label className="block caption top-margin">{a.position}</label>
      </div>
    ))}
    </div>
    <div className="report__authors__mobile">
      <span>by </span>
    {authors.map((a,i)=>(
      <span className="report__authors__item--mobile">
        <label>{`${a.first_name} ${a.last_name}`}</label>
        {(i==0 && authors.length==2) && <span> and </span>}
        {(i<authors.length-2 && authors.length>2) && <span>, </span>}
        {(i==authors.length-2 && authors.length>2) && <span>, and </span>}
      </span>
    ))}
    </div>
  </div>
);

export default Authors;
