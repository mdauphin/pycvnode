class Workflow {

  nodes : Array<SvgNode> ;
  connections : Array<Connection> ;

  constructor(svg : SVGSVGElement, data) {
    this.nodes = [];
    this.connections = [];
    this.loadNodes(svg,data);
    this.loadConnections(svg,data);
  }

  loadNodes(svg : SVGSVGElement, data) : void {
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

  loadConnections(svg : SVGSVGElement, data) : void {
    for (var connection of data.connections ) {
      var src = this.findNodeById(data.srcNodeId).findConnector(data.srcConnectorName);
      var dst = this.findNodeById(data.dstNodeId).findConnector(data.srcConnectorName);
      if( src != null && dst != null ) {
        var cnx = new Connection(svg,src,dst);
        this.connections.push(cnx);
      }
    }
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

class SvgNode extends SvgElement {

  name : string ;
  id : number ;
  g : SVGGElement ;
  rect : SVGDefsElement ;
  connectors : Array<Connector> ;

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

  findConnector( connectorName ) : Connector {
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
    var pt_loc = pt.matrixTransform(this.svg.getScreenCTM().inverse())
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

  getPosition() {
    return { 'x' : + this.x + this.getSize().width / 2, 'y' : + this.y + this.getSize().height / 2 }
  }

  selected( value : boolean ) {
    var color = '#848484' ;
    if( value )
      color = '#FF8000' ;
    this.rect.setAttributeNS(null,"fill",color);
  }
}

class Connector extends SvgElement {

  name : string ;
  parent : SvgNode ;
  g : SVGGElement ;
  circle : SVGCircleElement ;

  constructor( parent : SvgNode, data ) {
    super(parent.svg);
    this.parent = parent ;
    this.name = data.name ;
    this.generate();
  }

  public static create( parent : SvgNode, data ) : Connector {
    var type = data.dir as string;
    if ( type == "in" ) {
      return new ConnectorIn(parent,data);
    } else if( type == "out" ) {
      return new ConnectorOut(parent,data);
    }
    return null ; // Never append
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
    this.circle = <SVGCircleElement>this.createElementNS("circle", { 'cx' : x, 'cy' : y,
      'r' : 6,
      'fill' : 'yellow', 'stroke' : 'black',
       });
    this.g.appendChild(this.circle);
  }

  getSize() {
    return this.g.getBoundingClientRect();
  }

  getPosition() {
    return { 'x' : + this.circle.cx, 'y' : + this.circle.cy }
  }

}

class ConnectorIn extends Connector {

  connection : Connection ;

  constructor(parent : SvgNode, data) {
    super(parent,data);
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
    super(parent,data);
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
  connector_src : Connector ;
  connector_dst : Connector ;
  path : SVGPathElement ;

  constructor( svg : SVGSVGElement, src : Connector, dst : Connector ) {
    super(svg);
    this.connector_src = src ;
    this.connector_dst = dst ;
    this.path = <SVGPathElement>this.createElementNS("path", {
      'fill' : 'none',
      'stroke' : 'black',
    });
    svg.appendChild(this.path);
  }

  update = function() {
    var p1 = this.connector_src.getPosition();
    var p2 = this.connector_dst.getPosition();
    var pm = { 'x' : p1.x + ( p2.x - p1.x ) / 2, 'y' : p1.y + ( p2.y - p1.y ) / 2 };
    var path_d = "M" + p1.x + ',' + p1.y + ' '
      + 'C' + pm.x + ',' + p1.y + ' '
      + pm.x + ',' + p2.y + ' '
      +  p2.x + ',' + p2.y ;
    this.path.setAttributeNS(null,'d', path_d);
  }
}
