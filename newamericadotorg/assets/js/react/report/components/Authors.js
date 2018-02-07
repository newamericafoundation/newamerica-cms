const Authors = ({ authors }) => (
  <div className="report__authors">
    <div className="report__authors__desktop">
    <label className="block margin-top-0 margin-bottom-25">Authors</label>
    {authors.map((a)=>(
      <div className="report__authors__item margin-bottom-25">
        <label className="block bold">{`${a.first_name} ${a.last_name}`}</label>
        <label className="block caption">{a.position}</label>
      </div>
    ))}
    </div>
    <div className="report__authors__mobile">
      <span>by </span>
    {authors.map((a,i)=>(
      <span className="report__authors__item--mobile">
        <label className="bold">{`${a.first_name} ${a.last_name}`}</label>
        {(i==0 && authors.length==2) && <span> & </span>}
        {(i<authors.length-2 && authors.length>2) && <span>, </span>}
        {(i==authors.length-2 && authors.length>2) && <span> & </span>}
      </span>
    ))}
    </div>
  </div>
);

export default Authors;
