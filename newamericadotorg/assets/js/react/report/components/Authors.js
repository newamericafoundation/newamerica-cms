const Authors = ({ authors }) => (
  <div className="report__authors">
    <div className="report__authors__desktop">
    <label className="block margin-top-0 margin-bottom-25">Authors</label>
    {authors.map((a, i)=>(
      <div className="report__authors__item margin-bottom-25" key={`author-${i}`}>
        <label className="block bold"><a href={a.url}>{`${a.first_name} ${a.last_name}`}</a></label>
        <label className="block caption">{a.position}</label>
      </div>
    ))}
    </div>
    <div className="report__authors__mobile">
      <span>by </span>
    {authors.map((a,i)=>(
      <span className="report__authors__item--mobile" key={`author-${i}`}>
        <label className="bold"><a href={a.url}>{`${a.first_name} ${a.last_name}`}</a></label>
        {(i==0 && authors.length==2) && <span> & </span>}
        {(i<authors.length-2 && authors.length>2) && <span>, </span>}
        {(i==authors.length-2 && authors.length>2) && <span> & </span>}
      </span>
    ))}
    </div>
  </div>
);

export default Authors;
