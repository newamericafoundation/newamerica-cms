let social = [
  { label: 'Share', icon: 'fa-facebook', id: 'social__facebook' },
  { label: 'Tweet', icon: 'fa-twitter', id: 'social__twitter' },
  { label: 'Download', icon: 'fa-download', id: 'social__download'},
  { label: 'Print', icon: 'fa-print', id: 'social__print' }
];

const Social = () => (
  <div className="report__social">
    {social.map((s)=>(
      <div className={`report__social__item ${s.id}`}>
        <i className={`fa ${s.icon}`} />
        <label>{s.label}</label>
      </div>
    ))}
  </div>
);

export default Social;
