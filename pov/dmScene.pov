#include "colors.inc"
#include "stones.inc"
#include "textures.inc"
#include "shapes.inc"
#include "glass.inc"
#include "metals.inc"
#include "woods.inc"

#default {
	finish{
		ambient 0.0
		diffuse 0.9
	}
}

#declare BOX_SIZE = 4;
#declare BOX_HEIGHT = 2.75;
#declare EYE_Y = 1.5;

//----------------------------------------------------------------------
// camera
//----------------------------------------------------------------------
#macro makeCamera(Eye_y)
camera {
	//orthographic
	up<0,400,0>
	right<560,0,0>
	location <0, Eye_y, 0>
	look_at  <0, Eye_y, 3>
	angle 45
}
#end

//----------------------------------------------------------------------
// light
//----------------------------------------------------------------------
#macro makeLight(I)
light_source {
	<0, EYE_Y, 2>
	color <I,I,I> shadowless
}
#end

//----------------------------------------------------------------------
// Fog
//----------------------------------------------------------------------
#macro makeFog(D)
fog {
	lambda 2.0
	fog_type 1
	fog_offset 0.0
	fog_alt 0.0
	octaves 6
	omega 0.5
	turbulence <0,0,0>
	turb_depth 0.5
	up <0,1,0>
	
	distance D
	color <0.0,0.0,0.0>
}
#end


//----------------------------------------------------------------------
// Background (floor & roof)
//----------------------------------------------------------------------
#macro makeBg()
	plane {
		<0, 1, 0>,
		0
		hollow
		texture {
			T_Stone10
		}
	}

	plane {
		<0, 1, 0>,
		BOX_HEIGHT
		hollow
		texture {
			T_Stone10
		}
	}
#end

//----------------------------------------------------------------------
// Box
//----------------------------------------------------------------------
#declare Box = box {
	<-BOX_SIZE/2,0,-BOX_SIZE/2>, <BOX_SIZE/2,BOX_HEIGHT,BOX_SIZE/2>
	texture {
		brick texture{T_Stone8 }, texture{T_Stone10}
		scale <0.4,0.25,1>
		translate <0.0,0.1,0.0>
	}
}

#macro makeBox(X,Z)
	object { Box translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

//----------------------------------------------------------------------
// Face
//----------------------------------------------------------------------
#declare Face = box {
	<-BOX_SIZE/2,0,-0.001>, <BOX_SIZE/2,BOX_HEIGHT,0.001>
	texture {
		brick texture{T_Stone8 }, texture{T_Stone10}
		scale <0.4,0.25,1>
		translate <0,0.1,1>
	}
}

#macro makeFace(X,Z)
	object {Face translate<BOX_SIZE*X, 0, BOX_SIZE*Z+BOX_SIZE/2> }
#end
//----------------------------------------------------------------------
// Side
//----------------------------------------------------------------------
#macro makeSide(X,Z)
	#declare I = -1;
	#if (X>0)
		#declare I = 1;
	#end
	object {Face rotate <0,I*90,0> translate<BOX_SIZE*X-I*2, 0, BOX_SIZE*Z+BOX_SIZE> }
#end


//----------------------------------------------------------------------
// Doors
//----------------------------------------------------------------------
#declare DoorBox = difference {
	object{Box}
	object {
		box {
			<-1.2,-1,-50>, <1.2,2.5,50> 
			texture{T_Stone10}
		}
	}
}

#macro makeDoorBox(X,Z)
	object { DoorBox translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

#declare DoorWoodClosedBox = union {
	//object { DoorBox }
	// wooden door
	//object { box { <-1.2,2.5,-0.2>, <1.2,2.5,0.2> texture {P_WoodGrain1B translate <0,1.8,0>} translate <0,0,0>}}
	// wooden switch (right)
	object { box { <-0.1,-0.1,0.01>, <0.1,0.1,-0.01> texture {P_WoodGrain1B} translate <1.5,1.4,-2.0>}}
}



#macro makeDoorWoodClosedBox(X,Z)
	object { DoorWoodClosedBox translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

#macro makeDoorWoodClosedSideBox(X,Z)
	#declare I = -1;
	#if (X>0)
		#declare I = 1;
	#end
	
	object { DoorWoodClosedBox rotate <0,I*90,0> translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

//----------------------------------------------------------------------
// Niche
//----------------------------------------------------------------------
#declare Niche = difference {
	object{Box}
	object {
		box {
			<-1.2,0.5,-50>, <1.2,2,0> 
			texture{T_Stone10}
		}
	}
}

#macro makeNiche(X,Z)
	object { Niche translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

#macro makeNicheSide(X,Z)
	#declare I = -1;
	#if (X>0)
		#declare I = 1;
	#end
	
	object { Niche rotate <0,I*90,0> translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

//----------------------------------------------------------------------
// ItemBox
//----------------------------------------------------------------------
#declare ItemBox = box {
	<-0.75,0,-0.4>, <0.75,0.6,0.4>
	translate <-1.35, 0, 0.0>
	texture {
		T_Stone12
		scale <1,1,1>
		translate <0.0,0,0.0>
		rotate <0,25,0>
	}
}

#macro makeItemBox(X,Z)
	object { ItemBox translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

#macro makeItemBoxSide(X,Z)
	object { ItemBox rotate<0,-90,0> translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

//----------------------------------------------------------------------
// Dalle
//----------------------------------------------------------------------
#declare Dalle = box {
	<-BOX_SIZE/2,-0.001,-BOX_SIZE/2>, <BOX_SIZE/2,0,BOX_SIZE/2>
	texture {
		T_Stone10
	}
}

#macro makeDalle(X,Z)
	object { Dalle translate<BOX_SIZE*X, 0, BOX_SIZE*(Z+1)> }
#end

//----------------------------------------------------------------------
// Grid
//----------------------------------------------------------------------
#declare Grid = union {
	#declare s = 22;
	#declare I = -s;
	
	#while(I<s)
		object {cylinder { <I,0,-s>, <I,0,s>, 0.05 texture { pigment {White} } } }
		object {cylinder { <-s,0,I>, <s,0,I>, 0.05 texture { pigment {White} } } }
		#declare I = I+4;
	#end
}

global_settings { ambient_light rgb<0, 0, 0> }
