<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class DiagnosticoService
{
    protected $baseUrl;

    public function __construct()
    {
        // URL del servicio de IA dentro de Docker
        $this->baseUrl = rtrim(env('IA_API_URL'), '/');
    }

    public function generarDiagnostico(array $datos)
    {
        // Llamada POST a la IA con los datos
        $response = Http::post($this->baseUrl . '/diagnostico', $datos);

        if ($response->successful()) {
            return $response->json();
        }

        // Retorna error si no se pudo conectar
        return [
            'error' => 'No se pudo obtener el diagnóstico de la IA'
        ];
    }
}
