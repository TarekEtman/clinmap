import { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

/** Deterministic PRNG so the lattice is the same sculpture on every visit. */
function mulberry(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * The benchmark, as an object: 44 case-nodes in a loose organic shell,
 * paired by relation threads. Rust nodes are the flagged calls, and they breathe.
 */
function buildGraph() {
  const rand = mulberry(40);
  const nodes: { pos: THREE.Vector3; flagged: boolean }[] = [];
  for (let i = 0; i < 44; i++) {
    const theta = rand() * Math.PI * 2;
    const phi = Math.acos(2 * rand() - 1);
    const r = 2.05 + rand() * 1.55;
    nodes.push({
      pos: new THREE.Vector3(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta) * 0.72,
        r * Math.cos(phi)
      ),
      flagged: i % 7 === 3,
    });
  }
  const linePositions: number[] = [];
  for (let i = 0; i < nodes.length - 1; i += 2) {
    linePositions.push(...nodes[i].pos.toArray(), ...nodes[i + 1].pos.toArray());
  }
  for (let i = 0; i < 12; i++) {
    const a = Math.floor(rand() * nodes.length);
    const b = Math.floor(rand() * nodes.length);
    if (a !== b) linePositions.push(...nodes[a].pos.toArray(), ...nodes[b].pos.toArray());
  }
  return { nodes, linePositions: new Float32Array(linePositions) };
}

function Lattice() {
  const group = useRef<THREE.Group>(null);
  const { nodes, linePositions } = useMemo(buildGraph, []);
  const flaggedMats = useRef<Record<number, THREE.MeshStandardMaterial>>({});

  useFrame(({ clock, pointer }) => {
    const t = clock.getElapsedTime();
    if (group.current) {
      group.current.rotation.y = t * 0.055 + pointer.x * 0.22;
      group.current.rotation.x = Math.sin(t * 0.05) * 0.07 - pointer.y * 0.14;
    }
    Object.values(flaggedMats.current).forEach((m, i) => {
      m.emissiveIntensity = 0.55 + Math.sin(t * 1.5 + i * 1.9) * 0.4;
    });
  });

  const lineGeom = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    return g;
  }, [linePositions]);

  return (
    <group ref={group}>
      {nodes.map((n, i) => (
        <mesh key={i} position={n.pos}>
          <sphereGeometry args={[n.flagged ? 0.09 : 0.055, 24, 24]} />
          {n.flagged ? (
            <meshStandardMaterial
              ref={(m: THREE.MeshStandardMaterial | null) => {
                if (m) flaggedMats.current[i] = m;
              }}
              color="#A95F37"
              emissive="#A95F37"
              emissiveIntensity={0.6}
              roughness={0.3}
            />
          ) : (
            <meshStandardMaterial color="#344551" roughness={0.55} metalness={0.12} />
          )}
        </mesh>
      ))}
      <lineSegments geometry={lineGeom}>
        <lineBasicMaterial color="#94a3ad" transparent opacity={0.32} />
      </lineSegments>
    </group>
  );
}

export default function LatticeScene() {
  return (
    <Canvas
      dpr={[1, 1.8]}
      camera={{ position: [0, 0, 7.4], fov: 42 }}
      gl={{ antialias: true, alpha: true }}
      style={{ background: 'transparent' }}
    >
      <fog attach="fog" args={['#F7F4EF', 8.2, 13.5]} />
      <ambientLight intensity={0.95} />
      <directionalLight position={[4, 6, 5]} intensity={1.15} color="#fff4e2" />
      <directionalLight position={[-5, -2, -4]} intensity={0.45} color="#c7d4dc" />
      <Lattice />
    </Canvas>
  );
}
