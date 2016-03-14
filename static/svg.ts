class Workflow {

  nodes : Array<SvgNode> ;
  connections : Array<Connection> ;

  constructor(svg : SVGSVGElement, data) {
    this.nodes = [];
    this.connections = [];
    this.loadNodes(svg,data);
    this.loadConnections(svg,data);
  }

  private loadNodes(svg : SVGSVGElement, data) : void {
    for( var node of data.nodes ) {
      var n = new SvgNode(svg,node);
      this.nodes.push(n);
    }
  }

  findNodeById(id : number) : SvgNode {
    for(var i=0;i<this.nodes.length;i++) {
      if ( this.nodes[i].id == id ) {
        return this.nodes[i];
      }
    }
    return null;
  }

  private loadConnections(svg : SVGSVGElement, data) : void {
    for (var connection of data.connections ) {
      var src = <ConnectorOut>this.findNodeById(connection.src.id).findConnector(connection.src.name);
      var dst = <ConnectorIn>this.findNodeById(connection.dst.id).findConnector(connection.dst.name);
      if( src != null && dst != null ) {
        var cnx = new Connection(svg,src,dst);
        this.connections.push(cnx);
        cnx.update();
      }
    }
  }

  public removeConnection(cnx : Connection) {
    var elem = this.connections.filter( function(o) { return (o == cnx); } );
    if ( elem != null )
      cnx.remove();
  }
}

class SvgElement {

  svg : SVGSVGElement ;
  x : number ;
  y : number ;

  connectors : Array<Connector> ;

  constructor(svg : SVGSVGElement) {
    this.svg = svg ;
  }

  createElementNS(name : string, attributs = {}) : SVGDefsElement {
    var svgNS = "http://www.w3.org/2000/svg";
    var elem = document.createElementNS(svgNS,name);
    for( var item in attributs ) {
      elem.setAttributeNS(null, item, attributs[item] );
    }
    return (<SVGDefsElement>elem) ;
  }

  getSize() {
    return this.svg.getBoundingClientRect();
  }


}

enum Direction {
    Input,
    Output
}

interface IConnector {
  name : string ;
  dir : Direction ;
}

interface INode {
  id : number ;
  name : string ;
  connectors : Array<IConnector> ;
}

class SvgNode extends SvgElement implements INode {

  id : number ;
  name : string ;
  connectors : Array<Connector> ;

  g : SVGGElement ;
  rect : SVGDefsElement ;


  constructor( svg : SVGSVGElement, data ) {
    super(svg);
    this.id = data.id ;
    this.name = data.name ;
    this.connectors = [];

    this.generate();

    var dec = 50 ;
    for( var con of data.connectors ) {
      var tmp = Connector.create( this, con );
      var size = tmp.getSize();
      tmp.move(dec);
      this.connectors.push(tmp);
      dec += size.height + 5 ;
    }

    this.translate( data.x, data.y );
  }

  findConnector( connectorName ) : IConnector {
    for( var con of this.connectors ) {
      if ( con.name == connectorName ) {
        return con ;
      }
    }
    return null ;
  }

  //Generate svg code
  generate() {
    this.g = <SVGGElement>this.createElementNS('g');
    this.rect = this.createElementNS("rect", { 'rx' : 10, 'ry' : 10,
      'width' : 180, 'height' : 200,
      'fill' : '#848484', 'stroke' : 'black',
       });

    this.g.setAttributeNS(null,'onmousedown',"onMouseDown(evt);");
    //mouse selection is not match with g element !
    (<any>this.rect).data = this ;
    this.svg.appendChild(this.g);
    this.g.appendChild(this.rect);
    this.addText(this.name);
    this.addImage('/image/' + this.id )
  }

  addText(txt:string) {
    var text = this.createElementNS("text", { 'x':15, 'y':20, 'fill' : 'black' });
    text.textContent = txt ;
    this.g.appendChild(text);
  }

  addImage( url : string ) {
    var img = this.createElementNS("image", { 'x' : 10, 'y' : 40, 'width' : 128, 'height' : 128 });
    img.setAttributeNS('http://www.w3.org/1999/xlink', "href", url );
    this.g.appendChild(img);
  }

  move( x : number, y : number ) {
    var pt = this.svg.createSVGPoint();
    pt.x = x ; pt.y = y ;
    //transform global point to svg referential
    var pt_loc = pt.matrixTransform(this.svg.getScreenCTM().inverse());
    this.x = pt_loc.x - this.getSize().width / 2 ;
    this.y = pt_loc.y - this.getSize().height / 2 ;
    this.translate(this.x,this.y);
  }

  public translate( x:number, y:number ) {
    var translate = '(' + x + ',' + y  + ')';
    this.g.setAttribute('transform','translate' + translate );
  }

  public appendChild( child : SVGElement ) {
    this.g.appendChild(child);
  }

  getSize() {
    return this.g.getBoundingClientRect();
  }

  getPosition() : SVGPoint {
    return new SVGPoint();
    //return { 'x' : + this.x + this.getSize().width / 2, 'y' : + this.y + this.getSize().height / 2 }
  }

  selected( value : boolean ) {
    var color = '#848484' ;
    if( value )
      color = '#FF8000' ;
    this.rect.setAttributeNS(null,"fill",color);
  }
}

class Connector extends SvgElement implements IConnector {

  name : string ;
  dir : Direction ;

  parent : SvgNode ;
  g : SVGGElement ;
  circle : SVGCircleElement ;

  constructor( parent : SvgNode, dir : Direction, data ) {
    super(parent.svg);
    this.parent = parent ;
    this.name = data.name ;
    this.generate();
  }

  public static create( parent : SvgNode, data ) : Connector {
    var strtype : string = data.dir;
    var type : Direction = Direction[strtype];
    if ( type == Direction.Input ) {
      return new ConnectorIn(parent,data);
    } else if( type == Direction.Output ) {
      return new ConnectorOut(parent,data);
    }
    throw new Error("Connector type must be Direction.Input or Direction.Output")
  }

  generate() {
    //this.g = <SVGGElement>this.createElementNS('g');
    //this.parent.appendChild(this.g);
    //this.addCircle(6,0);
    //this.addText(this.name,15,4);
    console.log('Connector.generate() not be call !');
  }

  move( y : number ) {
    var x = 0 ;
    var translate = '(' + x + ',' + y  + ')';
    this.g.setAttribute('transform','translate' + translate )
  }

  addText(txt:string, x:number, y:number) {
    var text = this.createElementNS("text", { 'x':x, 'y':y, 'fill' : 'black' });
    text.textContent = txt ;
    this.g.appendChild(text);
  }

  addCircle(x:number,y:number) {
    this.circle = <SVGCircleElement>this.createElementNS("circle",
    { 'cx' : x, 'cy' : y,
      'r' : 6,
      'fill' : 'yellow', 'stroke' : 'black',
       });
    this.g.appendChild(this.circle);
  }

  /** Get the bouding rect of connector correpoding to g element */
  getSize() {
    return this.g.getBoundingClientRect();
  }

  /** Get the point of Connector relative to svg element */
  getPosition() : SVGPoint {
    var ctm = this.circle.getCTM();
    var pt = this.svg.createSVGPoint() ;
    return pt.matrixTransform(ctm);
  }

}

class ConnectorIn extends Connector {

  connection : Connection ;

  constructor(parent : SvgNode, data) {
    super(parent,Direction.Input,data);
    this.connection = null ;
  }

  generate() {
    this.g = <SVGGElement>this.createElementNS('g');
    this.parent.appendChild(this.g);
    this.addCircle(6,0);
    this.addText(this.name,15,4);
  }
}

class ConnectorOut extends Connector {

  connections : Array<Connection> ;

  constructor(parent : SvgNode, data) {
    super(parent,Direction.Output,data);
    this.connections = [];
  }

  generate() {
    this.g = <SVGGElement>this.createElementNS('g');
    this.parent.appendChild(this.g);
    //180 is parent width
    this.addCircle(180,0);
    this.addText(this.name,15,4);
  }
}

class Connection extends SvgElement {
  connector_src : ConnectorOut ;
  connector_dst : ConnectorIn ;
  path : SVGPathElement ;

  constructor( svg : SVGSVGElement, src : ConnectorOut, dst : ConnectorIn ) {
    super(svg);
    this.connector_src = src ;
    this.connector_dst = dst ;
    this.path = <SVGPathElement>this.createElementNS("path", {
      'fill' : 'none',
      'stroke' : 'black',
    });
    svg.appendChild(this.path);

    //Set connectors link
    this.connector_src.connections.push(this) ;
    this.connector_dst.connection = this ;
  }

  remove() {
    this.svg.removeChild(this.path);
    delete this.connector_src.connections[<any>this];
    this.connector_dst.connection = null ;
  }

  update() : void {
    var p1 = this.connector_src.getPosition();
    var p2 = this.connector_dst.getPosition();
    console.log( this.connector_src.name + ' ' + p1.x  + ' ' + p1.y );
    console.log( this.connector_dst.name + ' ' +  p2.x  + ' ' + p2.y );
    var pm = { 'x' : p1.x + ( p2.x - p1.x ) / 2, 'y' : p1.y + ( p2.y - p1.y ) / 2 };
    var path_d = "M" + p1.x + ',' + p1.y + ' '
      + 'C' + pm.x + ',' + p1.y + ' '
      + pm.x + ',' + p2.y + ' '
      +  p2.x + ',' + p2.y ;
    this.path.setAttributeNS(null,'d', path_d);
  }
}
