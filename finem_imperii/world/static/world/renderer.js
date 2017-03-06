function MapRenderer(regions, region_callback, settlement_callback, click_callback, focus_region_id, focus_settlement_id, show_region_tags) {

    container = document.createElement( 'div' );
    document.body.appendChild( container );

    //scene
    var scene = new THREE.Scene();

    //camera
    //var aspect = window.innerWidth / window.innerHeight;
    //var d = 5;
    //var camera = new THREE.OrthographicCamera( - d * aspect, d * aspect, d, - d, 1, 1000 );

    var camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 2.5;
    camera.position.x = 2.5;
    camera.position.y = 12;
    camera.lookAt(new THREE.Vector3( 0, 0, 0 ));
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    //renderer
    var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor( 0xffffff, 0);
    //controls
    if (focus_region_id === undefined) {
        var controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.addEventListener( 'change', render );
    }

    //ambient light
    var ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
    scene.add(ambientLight);
    //directional light
    var directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1).normalize();
    scene.add(directionalLight);

    //show canvas
    container.appendChild(renderer.domElement);

    var region_geometry = new THREE.CubeGeometry(1, 1, 1);
    var region_materials = {
        "plains": new THREE.MeshLambertMaterial({color: 0x90CD00, shading: THREE.SmoothShading}),
        "forest": new THREE.MeshLambertMaterial({color: 0x207F07, shading: THREE.SmoothShading}),
        "shore": new THREE.MeshLambertMaterial({color: 0x0D81CD, shading: THREE.SmoothShading}),
        "deepsea": new THREE.MeshLambertMaterial({color: 0x000E85, shading: THREE.SmoothShading}),
        "mountain": new THREE.MeshLambertMaterial({color: 0x837D71, shading: THREE.SmoothShading}),
    };

    for (var i = 0; i < regions.length; i++)  {
        var region = regions[i];
        var mesh = new THREE.Mesh(region_geometry, region_materials[region.type]);
        var geo = new THREE.EdgesGeometry( mesh.geometry ); // or WireframeGeometry
        var mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 1 } );
        var wireframe = new THREE.LineSegments( geo, mat );
        mesh.add( wireframe );

        mesh.position.x = region.x_pos - 1;
        mesh.position.z = region.z_pos - 1;
        mesh.position.y = region.y_pos;

        regions[i].mesh = mesh;
        mesh.region = regions[i];

        scene.add(mesh);

        if (focus_region_id == region.id) {
            camera.position.x = mesh.position.x;
            camera.position.y = 4;
            camera.position.z = mesh.position.z;
            camera.lookAt(mesh.position);
        }

        if (show_region_tags) {
            camera.updateMatrixWorld();
            camera.updateProjectionMatrix();

            var width = window.innerWidth, height = window.innerHeight;
            var widthHalf = width / 2, heightHalf = height / 2;

            var pos = mesh.position.clone();
            pos.y += 0.5;
            pos.project(camera);
            pos.x = ( pos.x * widthHalf ) + widthHalf;
            pos.y = -( pos.y * heightHalf ) + heightHalf;

            if (pos.x < width && pos.y < height) {
                var region_tag = document.createElement('div');
                region_tag.style.position = 'absolute';
                region_tag.style.width = "100px";
                region_tag.style.textAlign = "center";
                region_tag.style.height = 100;
                region_tag.style.background = "transparent";
                region_tag.innerHTML = region.name;
                region_tag.style.top = pos.y + 'px';
                region_tag.style.left = (pos.x - 50) + 'px';
                document.body.appendChild(region_tag);
            }
        }

        for (var j = 0; j < region.settlements.length; j++) {
            var settlement = region.settlements[j];

            var radius = Math.log10(settlement.population) * 0.02;
            var settlement_geometry = new THREE.CylinderGeometry( radius, radius, 0.01, 16 );
            var settlement_material;
            if (settlement.id == focus_settlement_id)
                settlement_material = new THREE.MeshBasicMaterial( {color: 0xFFFFFF} );
            else
                settlement_material = new THREE.MeshBasicMaterial( {color: 0x000000} );

            var cylinder = new THREE.Mesh( settlement_geometry, settlement_material );
            cylinder.position.x = (region.x_pos - 1) - 0.5 + settlement.x_pos/100;
            cylinder.position.z = (region.z_pos - 1) - 0.5 + settlement.z_pos/100;
            cylinder.position.y = region.y_pos + 0.5;

            cylinder.settlement = settlement;
            regions[i].settlements[j].mesh = cylinder;

            scene.add(cylinder);
        }
    }


    window.addEventListener( 'resize', onWindowResize, false );
    document.addEventListener( 'mousemove', onMouseMove, false );
    document.addEventListener( 'click', notify_click, false );

    var raycaster = new THREE.Raycaster();

    var mouse = new THREE.Vector2();

    function onMouseMove( event ) {
        if(region_callback === undefined && settlement_callback === undefined && click_callback === undefined)
            return
        // calculate mouse position in normalized device coordinates
        // (-1 to +1) for both components
        mouse.x = (event.clientX / window.innerWidth ) * 2 - 1;
        mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
        pick();
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize( window.innerWidth, window.innerHeight );
        render();
        pick();
    }

    var picked_region;
    var picked_settlement;

    function notify_click() {
        if (click_callback !== undefined) {
            return click_callback(picked_region, picked_settlement);
        }
    }

    function notify_region_pick(region) {
        if (region !== picked_region && region_callback !== undefined) {
            picked_region = region;
            return region_callback(region);
        }
    }

    function notify_settlement_pick(settlement) {
        if (settlement !== picked_settlement && settlement_callback !== undefined) {
            picked_settlement = settlement;
            return settlement_callback(settlement);
        }
    }

    function pick() {

        raycaster.setFromCamera( mouse, camera );

        // calculate objects intersecting the picking ray
        var intersects = raycaster.intersectObjects( scene.children );
        var region_intersected = false;
        var settlement_intersected = false;

        for ( var i = 0; i < intersects.length; i++ ) {

            var region = intersects[ i ].object.region;
            if (region !== undefined && !region_intersected) {
                notify_region_pick(region);
                region_intersected = true;
            }
            var settlement = intersects[ i ].object.settlement;
            if (settlement !== undefined && !settlement_intersected) {
                notify_settlement_pick(settlement);
                settlement_intersected = true;
            }

        }

        if (!settlement_intersected) notify_settlement_pick(undefined);
        if (!region_intersected) notify_region_pick(undefined);
    }

    //render scene
    function render() {
        renderer.render(scene, camera);
    }

    render();

}